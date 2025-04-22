FROM velvia/spark-jobserver:0.9.1-SNAPSHOT.mesos-1.0.0.spark-2.3.2.scala-2.11.jdk-8-jdk
RUN apt-get install -y python-pip && pip --no-cache-dir install pyhocon pyspark==2.3.2 py4j



# ===============================================================================
# Базовый образ (Java 11 обязателен для Spark 3.5.0)
# FROM eclipse-temurin:11-jdk

# # Установка зависимостей
# RUN apt-get update && apt-get install -y \
#     wget \
#     python3 \
#     python3-pip \
#     && rm -rf /var/lib/apt/lists/*

# # Скачивание и распаковка Spark
# RUN wget -q https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz \
#     && tar -xzf spark-3.5.0-bin-hadoop3.tgz -C /opt/ \
#     && mv /opt/spark-3.5.0-bin-hadoop3 /opt/spark \
#     && rm spark-3.5.0-bin-hadoop3.tgz

# # Установка PySpark (опционально)
# # RUN pip install pyspark==3.5.0

# # Настройка переменных окружения
# ENV SPARK_HOME=/opt/spark
# ENV PATH=$PATH:$SPARK_HOME/bin
# ENV PYSPARK_PYTHON=python3

# # Запуск Spark в standalone-режиме (опционально)
# # CMD ["/opt/spark/sbin/start-master.sh", "-h", "0.0.0.0"]
# # CMD ["/opt/spark/sbin/start-master.sh", "-d", "0.0.0.0"]
# # CMD ["/opt/spark/sbin/start-master.sh", "--host", "0.0.0.0", "--webui-port", "8080", ">>", "/var/log/spark.log", "2>&1", "&", "tail", "-f", "/dev/null"]

# # # Запуск Master в foreground + "tail" для удержания контейнера
# CMD /opt/spark/sbin/start-master.sh -h 0.0.0.0 && tail -f /opt/spark/logs/*




# ===============================================================================
# РАБОЧИЙ ВАРИАНТ
# FROM eclipse-temurin:11-jdk

# RUN apt-get update && apt-get install -y wget procps

# # Установка Spark
# RUN wget -q https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz \
#     && tar -xzf spark-3.5.0-bin-hadoop3.tgz -C /opt/ \
#     && mv /opt/spark-3.5.0-bin-hadoop3 /opt/spark \
#     && rm spark-3.5.0-bin-hadoop3.tgz

# # Запуск Master в foreground + "tail" для удержания контейнера
# CMD /opt/spark/sbin/start-master.sh -h 0.0.0.0 && tail -f /opt/spark/logs/*