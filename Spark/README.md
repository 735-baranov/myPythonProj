Для работы с Apache Spark:
1. Необходимо иметь настроенную сеть из нескольких машин (минимум 2)

2. На каждой машине должно быть установлено Java JDK

3. На каждую машину необходимо скачать архив Spark (https://spark.apache.org/downloads.html)
    + Если в дальнейшем будет производиться работа с python, лучше установить версию 2.3.3
    
4. После извлечения архива необходимо указать в Path пути до папок Java_Home и spark/bin

5. На машине, которая будет главным узлом кластера (Master) из командной строки (путь spark/bin/), необходимо запустить сервер
    + spark-class org.apache.spark.deploy.master.Master --ip "e.g 192.168.." --port "e.g 7070"
    
6. На каждом из остальных узлов, также из командной строки выполнить, указывая ip и порт главного узла
    + spark-class org.apache.spark.deploy.worker.Worker spark://"ip:port"
    
7. Для того, чтобы запустить задание можно воспользоваться встроенным интерпритатором python, java и т.д.
    + Тесты проводились в Pycharm
    
8. На главном узле в проекте PyCharm необходимо установить библиотеки pyspark, py4j

9. Также проекту необходимо сообщить о всех зависимостях интерпритатора, spark и т.д.
    + стабильно работает при добавлении зависимосттей напрямую (пример)
    
    #
    os.environ['SPARK_HOME']="X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7"

    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/bin")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python/pyspark/")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python/pyspark/sql")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python/pyspark/mllib")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python/lib")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python/lib/pyspark.zip")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python/lib/py4j-0.10.7-src.zip")
    sys.path.append("X:/Spark/Spark/spark-2.3.3-bin-hadoop2.7/spark-2.3.3-bin-hadoop2.7/python/lib/pyspark.zip")
    #

10. После, можно вызывать функции из тестовых примеров (папка tests)