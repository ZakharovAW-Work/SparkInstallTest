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
## Разворот **Spark-Кластера**

**Структура проекта**
```

```

### Создаем **Spark-master** и **Spark-worker**
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
