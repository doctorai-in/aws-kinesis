import sys
import boto3
import pyspark.sql.functions as F
from awsglue.transforms import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

session = boto3.Session()
glue_client = session.client(service_name='glue')

## @params: [JOB_NAME]
workflowName = 'walmartWorkflow'
workflow = glue_client.get_workflow(Name=workflowName)
workflow_params = workflow['Workflow']['LastRun']['WorkflowRunProperties']
workflowRunId = workflow['Workflow']['LastRun']['WorkflowRunId']
PROCESSED_BUCKET = workflow_params['processedBucket'] # s3://walmart_processed_data
LANDING_DB_NAME = workflow_params['kinesis_raw_db'] # orders
LANDING_DB_TABLE = workflow_params['kinesis_raw_dbTable'] # s3://orderlogs-doctorai/

orders = glueContext.create_dynamic_frame_from_catalog(LANDING_DB_NAME, LANDING_DB_TABLE, transformation_ctx = "orders")

ordersDF = orders.toDF()

ordersDF1 = ordersDF.select("Store", "Dept", "Weekly_Sales", "IsHoliday")

#ordersDF2 = ordersDF1.withColumnRenamed("stockcode","item_id").withColumnRenamed("quantity","demand").withColumnRenamed("storelocation","location").withColumnRenamed("invoicedate","timestamp")

ordersDF3 = ordersDF1.withColumn('Date',F.from_unixtime(F.unix_timestamp('Date', 'dd/mm/yyyy hh:mm:ss'),'yyyy-MM-dd HH:mm:ss'))

ordersDF4 = ordersDF3.repartition(1)

ordersDF4.write.csv("s3://"+PROCESSED_BUCKET+"/train/raw")

#productsDF1 = ordersDF.select("stockcode", "description", "unitprice")

#productsDF2 = productsDF1.withColumnRenamed("stockcode","item_id")

#productsDF3 = productsDF2.repartition(1)

#productsDF3.write.csv("s3://"+PROCESSED_BUCKET+"/products/raw")

client = boto3.client('s3')

response = client.list_objects(
    Bucket=PROCESSED_BUCKET,
    Prefix="train/raw"
)

ordersfile = response["Contents"][0]["Key"]
print(ordersfile)

client.copy_object(Bucket=PROCESSED_BUCKET, CopySource=PROCESSED_BUCKET+"/"+ordersfile, Key="train/train.csv")

client.delete_object(Bucket=PROCESSED_BUCKET, Key=ordersfile)

'''response = client.list_objects(
    Bucket=PROCESSED_BUCKET,
    Prefix="products/raw"
)

productsfile = response["Contents"][0]["Key"]
print(productsfile)

client.copy_object(Bucket=PROCESSED_BUCKET, CopySource=PROCESSED_BUCKET+"/"+productsfile, Key="products/product-data.csv")

client.delete_object(Bucket=PROCESSED_BUCKET, Key=productsfile)'''

