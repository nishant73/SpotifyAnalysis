# Spotify Analytics Pipeline on GCP

## Project Overview
This project builds an **end-to-end event-driven data pipeline** to extract, process, and analyze Spotify’s top 50 Bollywood songs. It leverages Google Cloud Platform (GCP) services for scalability, automation, and analytics. The pipeline follows the medallion architecture, processing data in bronze (cleaned) and gold (business-ready) layers, with results staged in BigQuery for analysis.

---

## Technology Stack
- **Programming Language**: Python
- **Cloud Platform**: Google Cloud Platform (GCP)
- **GCP Services**:
  - **Cloud Storage**: Compressive, scalable data storage
  - **Pub/Sub**: Asynchronous messaging between producer and consumer
  - **Cloud Run**: Serverless processing for event-driven functions
  - **Cloud Scheduler**: Cron jobs to schedule workflows
  - **Dataproc**: Apache Spark clusters for big data processing
  - **Cloud Composer**: Workflow orchestration using Apache Airflow
  - **BigQuery**: Data warehouse for analytics
  - **Looker**: Dashboard creation and data visualization

---

## Architecture Workflow
### Stage I: Data Extraction
1. **Spotify API Integration**:
   - Data pulled from Spotify API using a **Python script** deployed on **Cloud Run**.
   - Messages sent to a **Pub/Sub topic** for decoupled and scalable data processing.
2. **Storage**:
   - Data pushed to **Cloud Storage buckets** for logging and further processing.

### Stage II: Data Processing
1. **Bronze Layer**:
   - Data cleaned and converted from JSON to Parquet using **Dataproc Spark Job 1**.
   - Output stored in a separate Cloud Storage bucket.
2. **Gold Layer**:
   - Processed `artist` and `album` data from the bronze layer into gold using **Dataproc Spark Job 2**.
   - Extracted `track_info` data and staged it in **BigQuery** using **Dataproc Spark Job 3**.

### Stage III: Orchestration
1. **Cloud Composer (Airflow)**:
   - DAG (Directed Acyclic Graph) defined to orchestrate the pipeline.
   - Tasks include converting JSON files, combining data, and loading it into BigQuery.
   - Workflow dependencies managed to ensure seamless execution.

---

## Key Features
- **Event-Driven Data Pipeline**:
  - Asynchronous messaging with Pub/Sub.
  - Serverless execution using Cloud Run.
- **Medallion Architecture**:
  - Bronze layer: Cleaned data.
  - Gold layer: Analytics-ready data.
- **Workflow Automation**:
  - Scheduled and monitored with Cloud Composer.
  - Optimized processing workflows with PySpark jobs.
- **Scalable Analytics**:
  - Final data stored in BigQuery for large-scale analysis.
  - Visualized insights with Looker dashboards.

---

## Setup and Execution

### Prerequisites
1. **Spotify Developer Account**:
   - Sign up: [Spotify Developer Portal](https://developer.spotify.com/documentation/web-api)
   - Obtain Client ID and Client Secret.
2. **GCP Services**:
   - Enable APIs for Cloud Storage, Pub/Sub, Cloud Run, Cloud Scheduler, Dataproc, Cloud Composer, and BigQuery.

### Steps
#### Stage I: Data Extraction
1. **Create Pub/Sub Topic**:
   - Topic name: `Spotify-etl`
2. **Deploy Python Script to Cloud Run**:
   - Extract Spotify API data and publish messages to Pub/Sub topic.
3. **Create Subscription and Storage Bucket**:
   - Subscription filters relevant data.
   - Store raw JSON data in Cloud Storage.

#### Stage II: Data Processing
1. **Run Dataproc Spark Jobs**:
   - **Job 1**: Convert JSON to Parquet (bronze layer).
   - **Job 2**: Process `artist` and `album` data (gold layer).
   - **Job 3**: Extract `track_info` and publish to BigQuery.

#### Stage III: Orchestration
1. **Set up Cloud Composer DAG**:
   - Define tasks and dependencies for each stage.
   - Upload DAG to the `dags/` folder in Cloud Storage.
2. **Schedule Workflow**:
   - Use Cloud Composer to automate and monitor the pipeline.

---

## SQL Query for Verification
Once data is loaded into BigQuery, run the following query to verify:

```sql
SELECT *
FROM `YOUR-PROJECT-ID.SPOTIFY_ANALYTICS.TRACK_INFO`
ORDER BY artist_name;
```

---

## Output and Analytics
- **Processed Data**:
  - Stored in BigQuery for further analysis.
- **Visualization**:
  - Insights displayed through Looker dashboards.
