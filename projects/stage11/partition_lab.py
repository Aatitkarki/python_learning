"""11a/11b: bounded Python reference plus actual Spark partition/skew experiments."""
import argparse
import json
import time
from pathlib import Path

def streaming_totals(rows=1000000,batch_size=10000):
    if rows<0 or batch_size<1:raise ValueError('Invalid sizes')
    result={}
    for start in range(0,rows,batch_size):
        for i in range(start,min(start+batch_size,rows)):
            account=i%50;result[account]=result.get(account,0)+(i*17)%10000
    return {'rows':rows,'groups':len(result),'total_cents':sum(result.values()),'by_account':result,'maximum_batch_size':batch_size}

def spark_comparison(rows,output):
    import os,sys
    os.environ['PYSPARK_PYTHON']=sys.executable
    from pyspark.sql import SparkSession,functions as F,Window
    spark=SparkSession.builder.master('local[2]').appName('answer-partition-lab').config('spark.ui.enabled','false').getOrCreate()
    spark.sparkContext.setLogLevel('ERROR');reports=[];out=Path(output)
    try:
        for partitions in [2,8,32]:
            started=time.perf_counter()
            frame=spark.range(rows,numPartitions=partitions).selectExpr('id','id % 50 AS account','CAST((id*17)%10000 AS BIGINT) AS cents')
            aggregate=frame.groupBy('account').agg(F.sum('cents').alias('total'))
            totals={int(r.account):int(r.total) for r in aggregate.collect()}  # At most 50 result rows.
            assert totals==streaming_totals(rows)['by_account']
            (out/f'plan-{partitions}.txt').write_text(aggregate._jdf.queryExecution().toString())
            reports.append({'partitions':partitions,'seconds':time.perf_counter()-started,'total_cents':sum(totals.values())})
        skew=spark.range(rows).withColumn('key',F.when(F.col('id')%10!=0,F.lit(0)).otherwise(F.col('id')%50))
        skew_counts=skew.groupBy('key').count()
        salted=skew.withColumn('salt',F.col('id')%8).groupBy('key','salt').count().groupBy('key').agg(F.sum('count').alias('count'))
        assert {r.key:r['count'] for r in skew_counts.collect()}=={r.key:r['count'] for r in salted.collect()}
        dim=spark.range(50).withColumnRenamed('id','key').withColumn('label',F.concat(F.lit('account-'),F.col('key')))
        joined=skew.join(F.broadcast(dim),'key');assert joined.count()==rows
        (out/'broadcast-plan.txt').write_text(joined._jdf.queryExecution().toString())
        return {'runs':reports,'skew_counts':[r.asDict() for r in skew_counts.collect()],'salted_totals_match':True,'broadcast_join_rows':rows}
    finally:spark.stop()

def run(output,rows=1000000,spark=False):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);report={'python_reference':streaming_totals(rows)}
    if spark:report['spark']=spark_comparison(rows,out)
    else:report['spark_status']='Not run; pass --spark with Java and PySpark installed.'
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage11');p.add_argument('--rows',type=int,default=1000000);p.add_argument('--spark',action='store_true');a=p.parse_args();print(json.dumps(run(a.output,a.rows,a.spark),indent=2))
