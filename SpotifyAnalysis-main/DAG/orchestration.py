import datetime

from airflow import models
from airflow.models import Variable
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocSubmitSparkSqlJobOperator,
    DataprocSubmitPySparkJobOperator
)
from airflow.utils.dates import days_ago

project_id = Variable.get('project_id')
region = Variable.get('region')
bucket_name = Variable.get('bucket_name')
cluster_name = Variable.get('cluster_name')

default_args = {
    # Tell airflow to start one day ago, so that it runs as soon as you upload it
    "project_id": project_id,
    "region": region,
    "cluster_name": cluster_name,
    "start_date": days_ago(1)
}

with models.DAG(
    "spotify_analytics_pipeline",
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1)
) as dag:
    task_convert_album = DataprocSubmitSparkSqlJobOperator(
        task_id='run_convert_album',
        query_uri=f'gs://{bucket_name}/scripts/Bronze_layer_processing_album.py',
        variables={
            'bucket_name': f'gs://{bucket_name}',
            'table_name': 'album'
        },
    )

    task_convert_artist = DataprocSubmitSparkSqlJobOperator(
        task_id='run_convert_artist',
        query_uri=f'gs://{bucket_name}/scripts/Bronze_layer_processing_artist.py',
        variables={
            'bucket_name': f'gs://{bucket_name}',
            'table_name': 'artist'
        },
    )


    task_compute_track_info = DataprocSubmitSparkSqlJobOperator(
        task_id='run_track_info',
        query_uri=f'gs://{bucket_name}/scripts/gold_layer_processing.py',
        variables={
            'bucket_name': f'gs://{bucket_name}'
        },
    )

    task_load_track_info_bq = DataprocSubmitPySparkJobOperator(
        task_id='run_load_track_info_to_bq',
        main=f'gs://{bucket_name}/scripts/track_info_to_bq.py',
        dataproc_jars=['gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar']
                variables={
            'bucket_name': f'gs://{bucket_name}'
        },
    )
    


    task_convert_album >> task_compute_track_info
    task_convert_artist >> task_compute_track_info

    task_compute_track_info >> task_load_track_info_bq
    
