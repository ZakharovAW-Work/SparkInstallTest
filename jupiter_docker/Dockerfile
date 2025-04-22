# Базовый образ
FROM python:3.9-slim-buster           

# Вариант 2 - Установка Jupyter и зависимостей (если не используете готовый образ)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Установка PySpark и Jupyter
ARG SPARK_VERSION=3.5.0
ARG HADOOP_VERSION=3

RUN pip install --no-cache-dir \
    pyspark==${SPARK_VERSION} \
    jupyterlab \
    pandas \
    matplotlib

# Настройка переменных окружения
ENV SPARK_HOME=/usr/local/lib/python3.9/site-packages/pyspark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS='lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root'

# Рабочая директория
WORKDIR /home/jovyan/work

# Копируем ноутбуки (опционально)
COPY notebooks/ /home/jovyan/work/

# Порт Jupyter
EXPOSE 8888

# Запуск Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]