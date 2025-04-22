# Базовый образ (Java 11 или 17 обязательны для Spark 3.5.0)
FROM eclipse-temurin:17-jdk

# Переменные окружения (настраиваем версии и пути)
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=hadoop3
ENV SPARK_TGZ=spark-${SPARK_VERSION}-bin-${HADOOP_VERSION}.tgz
ENV SPARK_HOME=/opt/spark
# Путь к Python в venv
ENV PYSPARK_PYTHON=/opt/venv/bin/python3
# Добавляем venv в PATH
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:/opt/venv/bin

# Установка Python и wget
RUN apt-get update && apt-get install -y --no-install-recommends wget python3 python3-venv && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения
RUN python3 -m venv /opt/venv

# Активация виртуального окружения и установка PySpark
RUN /opt/venv/bin/pip install --no-cache-dir pyspark==${SPARK_VERSION}

# Скачивание и распаковка Spark
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_TGZ} \
    && tar -xzf ${SPARK_TGZ} -C /opt/ \
    && mv /opt/spark-${SPARK_VERSION}-bin-${HADOOP_VERSION} $SPARK_HOME \
    && rm ${SPARK_TGZ}


# Открываем порты (полезно для доступа к веб-интерфейсам)
EXPOSE 7077 4040 8080

# Запуск Spark в standalone-режиме (запуск master)
CMD ["/opt/spark/sbin/start-master.sh", "-h", "0.0.0.0"]



# # Базовый образ с Python и Java
# FROM python:3.9-slim

# # Установка Java (обязательно для Spark)
# RUN apt-get update && \
#     # apt-get install -y openjdk-11-jre-headless && \
#     apt-get install -y openjdk-11 && \
#     rm -rf /var/lib/apt/lists/*

# # Рабочая директория
# WORKDIR /app

# # Копируем зависимости и устанавливаем их
# COPY ./app/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Копируем весь код приложения
# COPY . .

# # Команда для запуска
# CMD ["python", "./app/main.py"]