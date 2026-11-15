from pathlib import Path
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import solution

ROOT=Path(__file__).resolve().parent
LOG_FILE=ROOT/"test_report.log"

def _log(no,name,status,expected=None,reason=None):
    if status=="PASS":
        line=f"Test Case {no:02d} : {name} : PASS"
    else:
        line=f"Test Case {no:02d} : {name} : FAIL | Expected = {expected} | Reason = {reason}"
    with open(LOG_FILE,"a",encoding="utf-8") as f: f.write(line+"\n")

def _run(no,name,expected,fn):
    try:
        fn(); _log(no,name,"PASS")
    except Exception as e:
        reason=str(e).replace("\n"," ") or e.__class__.__name__
        _log(no,name,"FAIL",expected,reason); raise


def test_01_load_vaccine_batches(spark):
    def body():
        df=solution.load_vaccine_batches(spark,str(ROOT/'data'/'vaccine_batches.csv'))
        d=dict(df.dtypes); assert df.count()==5, 'Expected 5 batch rows'; assert d['manufacture_date']=='date' and d['expiry_date']=='date', f'Wrong date types {d}'
    _run(1,'load_vaccine_batches','5 rows with both date columns as DateType',body)

def test_02_drop_incomplete_batches(spark):
    def body():
        schema='batch_id string, product_name string, manufacture_date date, expiry_date date, potency_pct double'
        df=spark.createDataFrame([('B1','A','2026-01-01','2027-01-01',98.0),('B2',None,'2026-01-01','2027-01-01',97.0)],'batch_id string, product_name string, manufacture_date string, expiry_date string, potency_pct double').withColumn('manufacture_date',to_date('manufacture_date')).withColumn('expiry_date',to_date('expiry_date'))
        out=solution.drop_incomplete_batches(df); assert out.count()==1 and out.first()['batch_id']=='B1', 'Only complete batch should remain'
    _run(2,'drop_incomplete_batches','Rows complete across required columns',body)

def test_03_add_stability_dates(spark):
    def body():
        df=spark.createDataFrame([('B1','2026-01-01','2027-01-01')],['batch_id','m','e']).withColumn('manufacture_date',to_date('m')).withColumn('expiry_date',to_date('e')).drop('m','e')
        r=solution.add_stability_dates(df).first()
        assert r['shelf_life_days']==365, f'Expected shelf life 365, got {r["shelf_life_days"]}'
        assert str(r['review_date'])=='2026-01-31', f'Expected review_date 2026-01-31, got {r["review_date"]}'
        expected=spark.range(1).select(datediff(current_date(),to_date(lit('2026-01-01'))).alias('d')).first()['d']
        assert r['days_since_manufacture']==expected, 'days_since_manufacture must use current_date'
    _run(3,'add_stability_dates','datediff/date_add/current_date derived columns',body)

def test_04_filter_potency_range(spark):
    def body():
        df=spark.createDataFrame([('B1',95.0),('B2',97.0),('B3',99.0)],['batch_id','potency_pct'])
        got={r['batch_id'] for r in solution.filter_potency_range(df,96.0,99.0).collect()}
        assert got=={'B2','B3'}, f'between must be inclusive, got {got}'
    _run(4,'filter_potency_range','Inclusive potency range',body)

def test_05_count_release_ready_batches(spark):
    def body():
        df=spark.createDataFrame([('RELEASED',98.0),('RELEASED',None),('HOLD',99.0)],['release_status','potency_pct'])
        assert solution.count_release_ready_batches(df)==1, 'Expected one RELEASED row with non-null potency'
    _run(5,'count_release_ready_batches','Python int count of RELEASED non-null-potency rows',body)

def test_06_count_release_ready_modified(spark):
    def body():
        df=spark.createDataFrame([('RELEASED',90.0),('RELEASED',91.0)],['release_status','potency_pct'])
        assert solution.count_release_ready_batches(df)==2, 'Count must change with modified input'
    _run(6,'count_release_ready_batches_modified','Dynamic DataFrame.count result',body)
