from flask import Flask, Response
import os
import subprocess

import json

app = Flask(__name__)


@app.route("/cat_stat", methods=["GET"])
def cat_stat():
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/cat_stat.py"

    os.environ[
        "SPARK_SUBMIT_ARGS"] = "--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar"

    result = subprocess.check_output(["/template.sh"])
    result = result.decode().split("ELIYAHELIYAHELIYAH\n")
    return Response(result[1], content_type="application/json")


@app.route("/prod_stat", methods=["GET"])
def prod_stat():
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/prod_stat.py"

    os.environ[
        "SPARK_SUBMIT_ARGS"] = "--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar"

    result = subprocess.check_output(["/template.sh"])
    result = result.decode().split("ELIYAHELIYAHELIYAH\n")

    return Response(result[1], content_type="application/json")




