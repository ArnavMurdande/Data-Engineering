# Databricks notebook source
# MAGIC %md
# MAGIC # Day 5 · Notebook 4 of 5 – ML extension with MLflow (long-stay risk)
# MAGIC
# MAGIC **Goal:** a small pilot that shows the full MLflow flow on Databricks:
# MAGIC
# MAGIC `feature table → train 2 models → log to MLflow → pick the best → register in Unity Catalog → set alias "champion" → score encounters → dashboard view`
# MAGIC
# MAGIC **Question the model answers:** at admission, is this encounter likely to become a **long stay** (length of stay above the 75th percentile)? Long stays drive bed pressure, so an early ranking helps bed managers plan.
# MAGIC
# MAGIC | Step | Output |
# MAGIC |---|---|
# MAGIC | 1 | Feature table `gold_schema.ml_encounter_features` |
# MAGIC | 2 | Quick look at the training data |
# MAGIC | 3 | Train logistic regression and random forest, log both runs to MLflow |
# MAGIC | 4 | Log the best model, register it as `gold_schema.long_stay_risk_model`, set alias `champion` |
# MAGIC | 5 | Score encounters into `gold_schema.encounter_long_stay_risk` and create `gold_schema.vw_encounter_long_stay_risk` |
# MAGIC | 6 | Limitations |
# MAGIC
# MAGIC **Run after** `09_1_dashboard_views`. **Cluster:** Databricks Runtime ML (has scikit-learn and MLflow).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
from mlflow import MlflowClient
from mlflow.models import infer_signature
from pyspark.sql import functions as F

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (precision_score, recall_score, f1_score, roc_auc_score,
                             confusion_matrix, ConfusionMatrixDisplay)

GOLD          = "capstone_8hospital.gold_schema"
FEATURE_TABLE = f"{GOLD}.ml_encounter_features"
RISK_TABLE    = f"{GOLD}.encounter_long_stay_risk"
MODEL_NAME    = f"{GOLD}.long_stay_risk_model"
LABEL         = "label_long_stay"

mlflow.set_registry_uri("databricks-uc")              # register models in Unity Catalog
user = spark.sql("SELECT current_user()").first()[0]
mlflow.set_experiment(f"/Users/{user}/capstone08_long_stay_risk")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1 – Feature table (one row per encounter)
# MAGIC * **Features** are only things known **at admission**: encounter type, triage priority, admission source, diagnosis group, department specialty and service level, department capacity, patient age band / sex / insurance type, admission hour and weekend flag.
# MAGIC * Outcome fields (`discharge_ts`, `encounter_status`, length of stay) are **not** features – they would leak the answer.
# MAGIC * **Label** `label_long_stay` = 1 if length of stay is above the 75th percentile of discharged encounters, else 0. Encounters without a discharge have no label yet (NULL). They are not used for training, only for scoring.
# MAGIC * `patient_id` is not used. Patient attributes come from `dim_patient` through the pseudonymised `patient_key`.

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {FEATURE_TABLE}
COMMENT 'Day 5 ML features per encounter (admission-time only); label = long stay (NULL when not discharged)'
AS
WITH threshold AS (
  SELECT percentile_approx(length_of_stay_hours, 0.75) AS p75
  FROM {GOLD}.fact_patient_encounter WHERE discharge_ts IS NOT NULL
)
SELECT f.encounter_id, f.admission_ts, to_date(f.admission_ts) AS admission_date,
       f.encounter_type, f.triage_priority,
       coalesce(f.admission_source, 'UNKNOWN')  AS admission_source,
       coalesce(f.diagnosis_group, 'UNKNOWN')   AS diagnosis_group,
       coalesce(d.specialty, 'UNKNOWN')         AS specialty,
       coalesce(d.service_level, 'UNKNOWN')     AS service_level,
       d.capacity_beds,
       coalesce(p.age_band, 'UNKNOWN')          AS age_band,
       coalesce(p.sex, 'UNKNOWN')               AS sex,
       coalesce(p.insurance_type, 'UNKNOWN')    AS insurance_type,
       hour(f.admission_ts)                     AS admission_hour,
       CAST(dayofweek(f.admission_ts) IN (1, 7) AS INT) AS is_weekend,
       t.p75                                    AS long_stay_threshold_hours,
       CASE WHEN f.discharge_ts IS NOT NULL THEN CAST(f.length_of_stay_hours > t.p75 AS INT) END AS {LABEL}
FROM {GOLD}.fact_patient_encounter f
CROSS JOIN threshold t
LEFT JOIN {GOLD}.dim_department d ON f.department_key = d.department_key
LEFT JOIN {GOLD}.dim_patient p    ON f.patient_key = p.patient_key
""")

display(spark.table(FEATURE_TABLE).agg(
    F.count("*").alias("rows"),
    F.count(LABEL).alias("labelled_rows"),
    F.sum(LABEL).alias("positives"),
    F.first("long_stay_threshold_hours").alias("long_stay_threshold_hours")))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2 – Look at the training data
# MAGIC Only labelled rows are used for training.

# COMMAND ----------

NUMERIC = ["capacity_beds", "admission_hour", "is_weekend"]
CATEGORICAL = ["encounter_type", "triage_priority", "admission_source", "diagnosis_group",
               "specialty", "service_level", "age_band", "sex", "insurance_type"]

train_pdf = spark.table(FEATURE_TABLE).filter(f"{LABEL} IS NOT NULL").orderBy("admission_ts").toPandas()
train_pdf[NUMERIC] = train_pdf[NUMERIC].astype(float)
train_pdf[LABEL] = train_pdf[LABEL].astype(int)

print("labelled rows:", len(train_pdf), "| days:", train_pdf["admission_date"].nunique())
print("class share (1 = long stay):", train_pdf[LABEL].value_counts(normalize=True).round(3).to_dict())

# a feature with only one value carries no information, so it is left out
constant = [c for c in NUMERIC + CATEGORICAL if train_pdf[c].nunique(dropna=True) <= 1]
NUMERIC_USED = [c for c in NUMERIC if c not in constant]
CATEGORICAL_USED = [c for c in CATEGORICAL if c not in constant]
FEATURES = NUMERIC_USED + CATEGORICAL_USED
print("left out (constant):", constant)
print("features used:", FEATURES)

display(train_pdf.groupby("encounter_type")[LABEL].agg(["count", "mean"]).reset_index())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3 – Train two models and log them to MLflow
# MAGIC * **Split:** time-based – train on the first 70% of admissions, test on the latest 30% (an out-of-time test). If the test part has only one class, a stratified random split is used instead.
# MAGIC * **Class imbalance:** both models use `class_weight="balanced"`.
# MAGIC * **Preprocessing** (fill missing values, scale numbers, one-hot encode categories) is inside the sklearn `Pipeline`, so the logged model takes the raw feature columns.
# MAGIC * **Logged per run:** parameters, precision / recall / F1 / ROC-AUC, confusion matrix image and feature importance.

# COMMAND ----------

X, y = train_pdf[FEATURES], train_pdf[LABEL]

cut = int(len(train_pdf) * 0.7)                               # rows are sorted by admission_ts
X_train, X_test, y_train, y_test = X.iloc[:cut], X.iloc[cut:], y.iloc[:cut], y.iloc[cut:]
SPLIT = f"time_based (test from {train_pdf['admission_ts'].iloc[cut]})"
if y_test.nunique() < 2 or y_train.nunique() < 2:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
    SPLIT = "stratified_random_30pct"
print("split:", SPLIT, "| train rows:", len(X_train), "| test rows:", len(X_test))


def build_pipeline(model):
    prep = ColumnTransformer([
        ("num", Pipeline([("fill", SimpleImputer(strategy="mean")), ("scale", StandardScaler())]), NUMERIC_USED),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_USED)])
    return Pipeline([("prep", prep), ("model", model)])


def feature_importance(pipe):
    names = pipe.named_steps["prep"].get_feature_names_out()
    model = pipe.named_steps["model"]
    values = model.feature_importances_ if hasattr(model, "feature_importances_") else np.abs(model.coef_[0])
    return pd.DataFrame({"feature": names, "importance": values}).sort_values("importance", ascending=False)


models = {
    "logistic_regression": LogisticRegression(class_weight="balanced", max_iter=2000, random_state=42),
    "random_forest": RandomForestClassifier(n_estimators=300, max_depth=6, min_samples_leaf=5,
                                            class_weight="balanced", random_state=42),
}

scores = []
for name, model in models.items():
    with mlflow.start_run(run_name=f"candidate_{name}"):
        pipe = build_pipeline(model).fit(X_train, y_train)
        prob = pipe.predict_proba(X_test)[:, 1]
        pred = (prob >= 0.5).astype(int)
        metrics = {"precision": precision_score(y_test, pred, zero_division=0),
                   "recall":    recall_score(y_test, pred, zero_division=0),
                   "f1":        f1_score(y_test, pred, zero_division=0),
                   "roc_auc":   roc_auc_score(y_test, prob)}

        mlflow.log_params({"model": name, "split": SPLIT, "n_features": len(FEATURES), "threshold": 0.5})
        mlflow.log_metrics(metrics)

        fig, ax = plt.subplots(figsize=(4, 4))
        ConfusionMatrixDisplay(confusion_matrix(y_test, pred, labels=[0, 1]),
                               display_labels=["normal stay", "long stay"]).plot(ax=ax, colorbar=False)
        ax.set_title(name)
        mlflow.log_figure(fig, "confusion_matrix.png")
        plt.close(fig)
        mlflow.log_table(feature_importance(pipe), "feature_importance.json")

        scores.append({"model": name, **{k: round(v, 4) for k, v in metrics.items()}})

scores_df = pd.DataFrame(scores)
display(scores_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4 – Log the best model, register it in Unity Catalog and set the alias `champion`
# MAGIC The best model (highest ROC-AUC, then F1) is trained again on **all** labelled rows and logged with a signature and an input example. Its holdout metrics from Step 3 are logged with it.
# MAGIC Every run of this cell creates a new model version, and the alias `champion` always points to the newest one.

# COMMAND ----------

best = scores_df.sort_values(["roc_auc", "f1"], ascending=False).iloc[0]
BEST = best["model"]
print("best model:", BEST, best.to_dict())

final_pipe = build_pipeline(clone(models[BEST])).fit(X, y)     # fresh copy, trained on all labelled rows
signature = infer_signature(X, final_pipe.predict_proba(X))

with mlflow.start_run(run_name=f"final_{BEST}"):
    mlflow.log_params({"model": BEST, "split": SPLIT, "n_features": len(FEATURES)})
    mlflow.log_metrics({f"holdout_{k}": best[k] for k in ["precision", "recall", "f1", "roc_auc"]})
    mlflow.set_tags({"project": "capstone08", "stage": "pilot", "data": "synthetic"})
    model_info = mlflow.sklearn.log_model(final_pipe, name="model", signature=signature,
                                          input_example=X.head(3), pyfunc_predict_fn="predict_proba")

registered = mlflow.register_model(model_info.model_uri, MODEL_NAME)
client = MlflowClient(registry_uri="databricks-uc")
client.set_registered_model_alias(MODEL_NAME, "champion", registered.version)
print(f"registered {MODEL_NAME} version {registered.version} with alias 'champion'")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5 – Score encounters and create the dashboard view
# MAGIC * The model is loaded **from the registry by alias**: `models:/capstone_8hospital.gold_schema.long_stay_risk_model@champion`.
# MAGIC * Scored: encounters that are **not discharged yet**. If every encounter is discharged, the encounters of the latest admission day are scored instead (for the demo).
# MAGIC * Risk bands: **HIGH** ≥ 0.6, **MEDIUM** ≥ 0.3, **LOW** < 0.3.
# MAGIC * The MERGE on `(encounter_id, score_date)` makes the cell safe to re-run.

# COMMAND ----------

champion = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@champion")

features = spark.table(FEATURE_TABLE)
to_score = features.filter(f"{LABEL} IS NULL")
if to_score.count() == 0:
    latest_day = features.agg(F.max("admission_date")).first()[0]
    to_score = features.filter(F.col("admission_date") == F.lit(latest_day))

score_pdf = to_score.toPandas()
score_pdf[NUMERIC] = score_pdf[NUMERIC].astype(float)
score_pdf["risk_score"] = champion.predict_proba(score_pdf[FEATURES])[:, 1].round(4)
score_pdf["risk_band"] = np.select([score_pdf["risk_score"] >= 0.6, score_pdf["risk_score"] >= 0.3], ["HIGH", "MEDIUM"], "LOW")
score_pdf["score_date"] = spark.sql("SELECT current_date()").first()[0]
score_pdf = score_pdf[["encounter_id", "score_date", "risk_score", "risk_band"]]

spark.sql(f"""CREATE TABLE IF NOT EXISTS {RISK_TABLE}
              (encounter_id STRING, score_date DATE, risk_score DOUBLE, risk_band STRING)
              COMMENT 'Day 5 pilot long-stay risk per encounter (see notebook 09_4 limitations)'""")
spark.createDataFrame(score_pdf).createOrReplaceTempView("new_scores")
spark.sql(f"""MERGE INTO {RISK_TABLE} t USING new_scores s
              ON t.encounter_id = s.encounter_id AND t.score_date = s.score_date
              WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *""")

print("encounters scored:", len(score_pdf))
display(spark.table(RISK_TABLE).filter("score_date = current_date()")
             .groupBy("risk_band").agg(F.count("*").alias("encounters"), F.round(F.avg("risk_score"), 4).alias("avg_score"))
             .orderBy("risk_band"))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW capstone_8hospital.gold_schema.vw_encounter_long_stay_risk
# MAGIC COMMENT 'Dashboard: pilot long-stay risk per encounter with department and encounter attributes (latest score date)'
# MAGIC AS
# MAGIC SELECT r.encounter_id, r.score_date, r.risk_score, r.risk_band,
# MAGIC        f.admission_ts, f.encounter_type, f.triage_priority, f.diagnosis_group,
# MAGIC        d.department_name, d.specialty, d.hospital_site
# MAGIC FROM capstone_8hospital.gold_schema.encounter_long_stay_risk r
# MAGIC JOIN capstone_8hospital.gold_schema.fact_patient_encounter f ON f.encounter_id = r.encounter_id
# MAGIC LEFT JOIN capstone_8hospital.gold_schema.dim_department d ON d.department_key = f.department_key
# MAGIC WHERE r.score_date = (SELECT max(score_date) FROM capstone_8hospital.gold_schema.encounter_long_stay_risk);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM capstone_8hospital.gold_schema.vw_encounter_long_stay_risk ORDER BY risk_score DESC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 6 – Limitations (say this in the demo)
# MAGIC * **Synthetic data.** The patterns are generated, not real clinical behaviour. Read the ROC-AUC from Step 3 honestly – a value near 0.5 means the features carry little signal.
# MAGIC * **Label is a choice.** "Long stay" = above the 75th percentile of this data set. A real definition must come from the clinical / bed-management owner.
# MAGIC * **Admission-time features only.** No vital signs, diagnosis codes or lab results – those would improve the model but must be available at the moment of scoring.
# MAGIC * **Sensitive attributes.** Age band and sex are used as features. Before any real use, a fairness review is needed (does the model treat groups differently for the same clinical need?).
# MAGIC * **Scores are a ranking, not a probability.** `class_weight="balanced"` shifts the scores up. Use the band to compare encounters, not as a clinical alarm.
# MAGIC * **Not production-ready.** It demonstrates the MLflow pipeline. Real use needs clinical validation, calibration, monitoring for drift and a governance sign-off.
# MAGIC
# MAGIC **Where to show MLflow in the demo:** *Experiments → capstone08_long_stay_risk* (compare the two candidate runs, open the confusion matrix) and *Catalog → capstone_8hospital → gold_schema → Models → long_stay_risk_model* (versions and the `champion` alias).