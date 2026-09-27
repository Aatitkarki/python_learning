"""Real Spark aggregation, trends, anomalies, windows, and Parquet output."""
import argparse
from pathlib import Path

def run(rows, output):
    import os, sys
    os.environ["PYSPARK_PYTHON"] = sys.executable
    from pyspark.sql import SparkSession, functions as F, Window
    spark=SparkSession.builder.master('local[2]').appName('transaction-lab').config('spark.ui.enabled','false').getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
    try:
        data=spark.range(rows).selectExpr('id','id % 50 AS account','CAST((id * 17) % 10000 AS BIGINT) AS cents','CAST(id / 1000 AS BIGINT) AS day')
        totals=data.groupBy('account').agg(F.sum('cents').alias('total_cents'),F.count('*').alias('count'))
        daily=data.groupBy('day').agg(F.sum('cents').alias('daily_cents'))
        window=Window.orderBy('day').rowsBetween(-2,0)
        trends=daily.withColumn('three_row_mean',F.avg('daily_cents').over(window))
        stats=data.agg(F.avg('cents').alias('mean'),F.stddev_pop('cents').alias('sd')).first()
        anomalies=data.where(F.abs(F.col('cents')-stats['mean'])>3*stats['sd'])
        output=Path(output)
        totals.write.mode('errorifexists').parquet(str(output/'totals'))
        trends.write.mode('errorifexists').parquet(str(output/'trends'))
        totals.explain()
        return {'rows':data.count(),'groups':totals.count(),'anomalies':anomalies.count(),
                'total_cents':totals.agg(F.sum('total_cents')).first()[0],
                'note':'Uniform synthetic amounts may produce zero 3-sigma anomalies; that is not a fraud detector.'}
    finally: spark.stop()

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--rows',type=int,default=100000); p.add_argument('--output',default='work/spark-run'); a=p.parse_args()
    if a.rows<1: p.error('rows must be positive')
    print(run(a.rows,a.output))
