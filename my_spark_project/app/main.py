from pyspark.sql import SparkSession



# spark = SparkSession \
#     .builder \
#     .appName("Python Spark SQL basic example") \
#     .config("spark.some.config.option", "some-value") \
#     .getOrCreate()


spark = SparkSession \
    .builder \
    .appName("DockerSparkApp") \
    .getOrCreate()

# Пример обработки данных
df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
df.show()

spark.stop()