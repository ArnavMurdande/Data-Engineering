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


def test_01_load_ad_impressions(spark):
    def body():
        df=solution.load_ad_impressions(spark,str(ROOT/'data'/'ad_impressions.csv')); d=dict(df.dtypes)
        assert df.count()==4, 'Expected 4 impression rows'; assert d['impression_ts']=='timestamp', 'impression_ts must be TimestampType'; assert d['watched_seconds']=='double' and d['spend_amount']=='double', f'Numeric casts missing {d}'
    _run(1,'load_ad_impressions','4 rows, timestamp conversion and numeric casts',body)

def test_02_join_campaign_metadata(spark):
    def body():
        i=spark.createDataFrame([('I1','C1',1.0),('I2','C9',2.0)],['impression_id','campaign_id','spend_amount']); c=spark.createDataFrame([('C1','Campaign A')],['campaign_id','campaign_name'])
        out=solution.join_campaign_metadata(i,c); assert out.count()==1 and out.first()['campaign_name']=='Campaign A', 'Expected inner join on campaign_id'
    _run(2,'join_campaign_metadata','Inner join with campaign fields',body)

def test_03_add_engagement_metrics(spark):
    def body():
        df=spark.createDataFrame([('I1',90.0,100.0),('I2',50.0,100.0),('I3',20.0,100.0),('I4',10.0,None)],['impression_id','watched_seconds','ad_length_seconds'])
        got={r['impression_id']:(float(r['watch_pct']),r['engagement_band']) for r in solution.add_engagement_metrics(df).collect()}
        assert got=={'I1':(90.0,'High'),'I2':(50.0,'Medium'),'I3':(20.0,'Low'),'I4':(0.0,'Low')}, f'Wrong engagement metrics {got}'
    _run(3,'add_engagement_metrics','watch_pct and High/Medium/Low classification',body)

def test_04_campaign_performance_summary(spark):
    def body():
        df=spark.createDataFrame([('I1','C1','A','DELIVERED','Y',2.0),('I2','C1','A','DELIVERED','N',3.0),('I3','C2','B','FAILED','Y',10.0)],['impression_id','campaign_id','campaign_name','delivery_status','clicked','spend_amount'])
        rows=solution.campaign_performance_summary(df).collect(); assert len(rows)==1, f'Expected one DELIVERED campaign row, got {rows}'
        r=rows[0]; assert r['impression_count']==2 and r['click_count']==1 and abs(float(r['total_spend'])-5.0)<1e-9, f'Wrong campaign summary {r}'
    _run(4,'campaign_performance_summary','DELIVERED count/click-count/spend aggregation',body)

def test_05_top_n_campaigns_by_spend(spark):
    def body():
        df=spark.createDataFrame([('C1','A',10.0,2,1),('C2','B',20.0,3,2),('C3','C',5.0,1,0)],['campaign_id','campaign_name','total_spend','impression_count','click_count'])
        rows=solution.top_n_campaigns_by_spend(df,2).collect(); assert [r['campaign_id'] for r in rows]==['C2','C1'], f'Wrong top-N ordering {rows}'
    _run(5,'top_n_campaigns_by_spend','Top n by spend descending',body)

def test_06_top_n_campaign_tie(spark):
    def body():
        df=spark.createDataFrame([('C2','B',10.0,1,0),('C1','A',10.0,1,0)],['campaign_id','campaign_name','total_spend','impression_count','click_count'])
        rows=solution.top_n_campaigns_by_spend(df,1).collect(); assert len(rows)==1 and rows[0]['campaign_id']=='C1', 'Tie must use campaign_id ascending before limit'
    _run(6,'top_n_campaigns_by_spend_tie','Deterministic tie ordering plus dynamic n',body)
