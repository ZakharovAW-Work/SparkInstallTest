import pyspark
import logging
import os

from pyspark.sql import SparkSession


# =================================================================================================

logging.basicConfig(level=logging.INFO,
                    filename=os.path.join('..', 'SparkInstallTest', 'logs', 'spark_logs.log'),
                    filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

spark = SparkSession.builder \
    .appName("LocalTest") \
    .master("spark://DESKTOP-SPM5Q5T.:7077") \
    .getOrCreate()

# =================================================================================================



df = spark.createDataFrame([('Alice', 1)]).show()

logging.info(df)

spark.stop()