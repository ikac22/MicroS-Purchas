from pyspark.sql import SparkSession
import pyspark.sql.functions as F
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

category_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shop") \
    .option("dbtable", "shop.category") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

product_category_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shop") \
    .option("dbtable", "shop.product_category") \
    .option("user", "root") \
    .option("password", "root") \
    .load()


product_order_data_frame = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shop") \
    .option("dbtable", "product_order") \
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

# people_data_frame.show ( )
# result = people_data_frame.filter ( people_data_frame["gender"] == "Male" ).collect ( )
# print ( result )

result = category_data_frame.join(
    product_category_data_frame,
    category_data_frame["id"] == product_category_data_frame["cid"]) \
    .join(product_order_data_frame,
          product_category_data_frame["pid"] == product_order_data_frame["pid"],
          how="outer") \
    .join(order_data_frame,
          order_data_frame["id"] == product_order_data_frame["oid"],
          how="outer"
          ) \
    .select(category_data_frame["name"], order_data_frame["status"], product_order_data_frame["quantity"])\
    .rdd.map(lambda x: (x[0], x[2]) if x[1] == "COMPLETE" else (x[0], 0))\
    .reduceByKey(lambda a, b: a + b)\
    .toDF(["name", "qsum"])\
    .sort(F.desc("qsum"), F.asc("name"))\
    .rdd.map(lambda x: x[0])\
    .collect()

result = json.dumps({"statistics": result}, indent=4)

print("ELIYAHELIYAHELIYAH")
print(result)
print("ELIYAHELIYAHELIYAH")
spark.stop()
