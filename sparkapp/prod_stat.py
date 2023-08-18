from pyspark.sql import SparkSession
import json

import os

PRODUCTION = True if ("PRODUCTION" in os.environ) else False
DATABASE_IP = os.environ["DATABASE_IP"] if ("DATABASE_IP" in os.environ) else "localhost"

builder = SparkSession.builder.appName("PySpark Database example")

if (not PRODUCTION):
    builder = builder.master("local[*]") \
        .config(
        "spark.driver.extraClassPath",
        "mysql-connector-j-8.0.33.jar"
    )

spark = builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

product_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shop") \
    .option("dbtable", "shop.product") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

product_order_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shop") \
    .option("dbtable", "shop.product_order") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

order_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shop") \
    .option("dbtable", "shop.order_stat") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

result = product_data_frame.join(
    product_order_data_frame,
    product_data_frame["id"] == product_order_data_frame["pid"],
    ) \
    .join(order_data_frame,
          order_data_frame["id"] == product_order_data_frame["oid"],
          ) \
    .select(product_data_frame["name"], order_data_frame["status"], product_order_data_frame["quantity"]) \
    .rdd.map(lambda x: \
                (x[0], (x[2], 0)) if x[1] == "COMPLETE"
                else (x[0], (0, x[2])) if x[1] == "CREATED" or x[1] == "PENDING" else (x[0], (0, 0)))\
    .reduceByKey(lambda a, b:  (a[0]+b[0], a[1]+b[1]))\
    .map(lambda x: (x[0], x[1][0], x[1][1])).toDF(["name", "sold", "waiting"]).toJSON().collect()

result = {"statistics": list(map(lambda x: json.loads(x), result))}
result = json.dumps(result, indent=4)
print("ELIYAHELIYAHELIYAH")
print(result)
print("ELIYAHELIYAHELIYAH")
spark.stop()
