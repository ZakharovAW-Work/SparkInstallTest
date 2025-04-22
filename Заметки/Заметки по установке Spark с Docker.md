## **Основные шаги**
### 1. Установить wsl
```bash
wsl.exe --install Ubuntu-24.04
```
На месте `Ubuntu-24.04` Можно указать ваш дистрибутив.

**Или другой вариант:**
```bash
wsl --install -d Ubuntu
```

### 2. Скачать и установить Docker

Ссылка для скачивания:
https://www.docker.com/

Не забывай включить виртуализацию в **Bios**
#### 2.1 В Docker Desktop включить поддержку wsl

Знак настройки - Resourses - WSL integration - Включить поддержку подсистемы.

### 3. Создать директорию с файлом `Dockerfile`
```bash
mkdir SparkTestInstall
> Dockerfile
```

---
## Установка **PySpark** (локально)

**Ставим Python**
```bash
sudo apt update
sudo apt install python3.12
```

**Ставим venv**
```bash
sudo apt install python3.12-venv
```

**Создаем и активируем venv**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Ставим jdk
```bash
sudo apt-get install openjdk-17-jdk
```

**Ставим PySpark
```bash
pip install pyspark
```

**Ставим ipykernel
```bash
pip install ipykernel
```

Код для теста:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("dgbgfgd").getOrCreate()
data = [
    {
    'name': 'AAA',
    'id': 1
    },
    {
    'name': 'BBB',
    'id': 2
    }
]

df = spark.createDataFrame(data)
df.show()
spark.stop()
```
Вывод:
```bash
+---+----+
| id|name|
+---+----+
|  1| AAA|
|  2| BBB|
+---+----+
```



---
## Вариант с **Dockerfile**
### 3. Заполняем Dockerfile

```Dockerfile
# Базовый образ (Java 11 обязателен для Spark 3.5.0)
FROM eclipse-temurin:11-jdk

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Скачивание и распаковка Spark
RUN wget -q https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz \
    && tar -xzf spark-3.5.0-bin-hadoop3.tgz -C /opt/ \
    && mv /opt/spark-3.5.0-bin-hadoop3 /opt/spark \
    && rm spark-3.5.0-bin-hadoop3.tgz

# Установка PySpark (опционально)
RUN pip install pyspark==3.5.0

# Настройка переменных окружения
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYSPARK_PYTHON=python3

# Запуск Spark в standalone-режиме (опционально)
CMD ["/opt/spark/sbin/start-master.sh", "-h", "0.0.0.0"]
```

### 4. Собираем и запускаем контейнер
```bash
docker build -t my-spark:3.5.0 .
docker run -it -p 4040:4040 -p 8080:8080 my-spark:3.5.0
```

- `4040` — порт Spark UI (для мониторинга задач)
- `8080` — порт веб-интерфейса Spark Master

**Доступ к веб-интерфейсу**  
- http://localhost:8080 (Spark Master) 
- http://localhost:4040 (задачи Spark)

### 5. 


---
## Вариант с **docker-compose**

**Содержимое файла docker-compose.yaml**:
```yaml
version: "3"

services:
  spark-iceberg:
    image: tabulario/spark-iceberg
    container_name: spark-iceberg
    build: spark/
    networks:
      iceberg_net:
    depends_on:
      - rest
      - minio
    volumes:
      - ./warehouse:/home/iceberg/warehouse
      - ./notebooks:/home/iceberg/notebooks/notebooks
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
    ports:
      - 8888:8888
      - 8080:8080
      - 10000:10000
      - 10001:10001
  rest:
    image: apache/iceberg-rest-fixture
    container_name: iceberg-rest
    networks:
      iceberg_net:
    ports:
      - 8181:8181
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
      - CATALOG_WAREHOUSE=s3://warehouse/
      - CATALOG_IO__IMPL=org.apache.iceberg.aws.s3.S3FileIO
      - CATALOG_S3_ENDPOINT=http://minio:9000
  minio:
    image: minio/minio
    container_name: minio
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=password
      - MINIO_DOMAIN=minio
    networks:
      iceberg_net:
        aliases:
          - warehouse.minio
    ports:
      - 9001:9001
      - 9000:9000
    command: ["server", "/data", "--console-address", ":9001"]
  mc:
    depends_on:
      - minio
    image: minio/mc
    container_name: mc
    networks:
      iceberg_net:
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
    entrypoint: |
      /bin/sh -c "
      until (/usr/bin/mc config host add minio http://minio:9000 admin password) do echo '...waiting...' && sleep 1; done;
      /usr/bin/mc rm -r --force minio/warehouse;
      /usr/bin/mc mb minio/warehouse;
      /usr/bin/mc policy set public minio/warehouse;
      tail -f /dev/null
      "
networks:
  iceberg_net:
```

**Запуск docker-compose**
```bash
docker-compose up
```

**Адрес сеанса Spark** (Для проверки запуска)
```
http://localhost:8888
```

