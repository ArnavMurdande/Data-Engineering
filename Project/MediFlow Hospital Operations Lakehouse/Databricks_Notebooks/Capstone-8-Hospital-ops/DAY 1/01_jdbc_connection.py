# Databricks notebook source
# DBTITLE 1,Read patient_master via JDBC with secrets
jdbc_url = (
    "jdbc:sqlserver://capstone8dbserver.database.windows.net:1433;"
    "database=capstone8;"
    "encrypt=true;"
    "trustServerCertificate=false;"
    "hostNameInCertificate=*.database.windows.net;"
    "loginTimeout=30;"
)

SECRET_SCOPE = "azure-sql-scope"
jdbc_user = dbutils.secrets.get(scope=SECRET_SCOPE, key="sql-user")
jdbc_password = dbutils.secrets.get(scope=SECRET_SCOPE, key="sql-pwd")

try:
    df = (spark.read
        .format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", "dbo.patient_master")
        .option("user", jdbc_user)
        .option("password", jdbc_password)
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
        .load())
    display(df)
except Exception as e:
    print(str(e)[:2000])

# COMMAND ----------

# DBTITLE 1,Read department_master via JDBC
try:
    df1 = (spark.read
        .format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", "dbo.department_master")
        .option("user", jdbc_user)
        .option("password", jdbc_password)
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
        .load())
    display(df1)
except Exception as e:
    print(str(e)[:2000])

# COMMAND ----------

# DBTITLE 1,Read bed_master via JDBC
try:
    df2 = (spark.read
        .format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", "dbo.bed_master")
        .option("user", jdbc_user)
        .option("password", jdbc_password)
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
        .load())
    display(df2)
except Exception as e:
    print(str(e)[:2000])

# COMMAND ----------

catalog = "capstone_8hospital"
schema = "bronze_schema"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.bronze_patients")
df1.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.bronze_departments")
df2.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.bronze_beds")