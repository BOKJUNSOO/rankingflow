from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import datetime
import pendulum
