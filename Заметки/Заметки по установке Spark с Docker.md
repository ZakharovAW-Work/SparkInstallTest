## **Основные шаги.**
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

### 4. Опционально. Монтирование диска к WSL

**Создаем точку (папку) монтирования**
```bash
sudo mkdir /mount-disk
```

**Монтируем дик**
```bash
sudo mount -t drvfs D: mount-disk
```

**Прокидываем репозиторий git**
```bash
git config --global --add safe.directory /mount-disk/Work/SparkInstallTest
```



---
## Установка **PySpark** (локально). Для тестирования.

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
## Запуск **Jypiter** в Docker

Создаем директорию "jupiter_docker/notebooks".
В **jupiter_docker** создаем **Dockerfile**
```Dockerfile
# Базовый образ (выберите один)
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
```

**Собираем образ**
```bash
docker build -t jupyter-pyspark:latest .
```

В **jupiter_docker** создаем **docker-compose.yaml:**
```yaml
version: '3'
services:
  jupyter:
    # image: jupyter/datascience-notebook
    image: jupyter-pyspark:latest
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/work  # Монтирование папки
    environment:
      - JUPYTER_TOKEN=mysecretpassword  # Пароль для доступа
```

**Запускаем контейнер**
```bash
docker-compose up -d
```

**Теперь можем подключиться к Jypiter Server по адресу:**
`http://localhost:8888/`

**И ввести пароль** 
`mysecretpassword`

**Или в VScode:**
`select cernel -> Existing Jypiter Server -> Ввести http://localhost:8888/ и пароль`


---
## Запуск **Spark-Кластера.**

**Структура проекта**
```
├── spark_client
│   ├── client_1.py
│   └── client_2.ipynb
├── spark_cluster
│   └── docker-compose.yaml
├── venv_wsl
```  

Для выбора интерпретатора в VSCode нажать `ctr+shift+p` и ввести `python: select interpreter`, далее выбрать тот, что указан в наше venv_wsl.

### Вариант без **Docker (Standalone - режим)**

**Скачиваем архив spark:** 
```bash
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
```

**Распаковываем:**
```bash
tar -xzf spark-3.5.0-bin-hadoop3.tgz
```

Переходим в `spark-3.5.0-bin-hadoop3`.

**Запускаем** `master`
```bash
sbin/start-master.sh
```
В браузере по `http://localhost:8080/` должна быть доступна страница spark. 
Тут же смотрим адрес `spark://DESKTOP-SPM5Q5T.:7077`.


**Запускаем** `worker`
```bash
sbin/start-worker.sh spark://DESKTOP-SPM5Q5T.:7077
```

В файле `client.py`:
```python
spark = SparkSession.builder \
    .appName("LocalTest") \
    .master("spark://DESKTOP-SPM5Q5T.:7077") \
    .getOrCreate()

df = spark.createDataFrame([('Alice', 1)]).show()

spark.stop()
```

Получаем
```
+-----+---+                                                                     
|   _1| _2|
+-----+---+
|Alice|  1|
+-----+---+
```

Для **остановки**:
```bash
sbin/stop-worker.sh
sbin/stop-master.sh
```


В `client_2.ipynb` прописываем:
```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("RemoteApp") \
    .master("spark://DESKTOP-SPM5Q5T.:7077") \
    .config("spark.driver.host", "localhost") \
    .config("spark.driver.bindAddress", "0.0.0.0") \
    .config("spark.executor.memory", "1g") \
    .getOrCreate()
```



### Создаем **Spark-master** и **Spark-worker**, используя **Docker**.
**Содержимое файла docker-compose.yaml**:
```yaml
version: '3'
services:
  spark-master:
    image: bitnami/spark:3.5
    ports:
      - "8080:8080"  # Web UI
    environment:
      - SPARK_MODE=master

  spark-worker:
    image: bitnami/spark:3.5
    depends_on:
      - spark-master
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
```

**Запуск docker-compose**
```bash
docker-compose up -d
```

**Адрес сеанса Spark** (Для проверки запуска)
```
http://localhost:8080
```


### Заполняем **Dockerfile** (Клиент)

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
