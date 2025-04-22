from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("DockerSparkApp") \
    .master("spark://spark-master:7077") \  
    .config("spark.executor.memory", "1g") \
    .getOrCreate()

# Пример обработки данных
df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
df.show()

spark.stop()