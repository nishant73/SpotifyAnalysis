import os
from pyspark.sql import SparkSession

spark = SparkSession. \
    builder. \
    getOrCreate()

data_uri = os.environ.get('DATA_URI') # your gold layer gcs bucket 
project_id = os.environ.get('PROJECT_ID') # your gcp-project-id
dateset_name = os.environ.get('DATASET_NAME') # your-biquery dataset
gcs_temp_bucket = os.environ.get('GCS_TEMP_BUCKET') # your temp staging bucket for processing before pusblishing into bigquery

track_info = spark. \
    read. \
    parquet(data_uri)

spark.conf.set('temporaryGcsBucket', gcs_temp_bucket)

track_info. \
    write. \
    mode('overwrite'). \
    format('bigquery'). \
    option('table', f'{project_id}:{dateset_name}.TRACK_INFO'). \
    save()