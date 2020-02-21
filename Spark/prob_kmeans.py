import os
import sys

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

from __future__ import print_function

import numpy as np
from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans


def parseVector(line):
    return np.array([float(x) for x in line.split(' ')])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kmeans <file> <k>", file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName="KMeans")
    lines = sc.textFile(sys.argv[1])
    data = lines.map(parseVector)
    k = int(sys.argv[2])
    model = KMeans.train(data, k)
    print("Final centers: " + str(model.clusterCenters))
    print("Total Cost: " + str(model.computeCost(data)))
    sc.stop()
