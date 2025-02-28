# Step 1: Create bronze layer DB
spark.sql("""
CREATE DATABASE IF NOT EXISTS album_bronze_db 
LOCATION 'your-bucket-name';
""")

# Step 2: Use the Database (Set the current database context)
spark.sql("USE album_bronze_db;")

# Step 3: Create a Temporary View from the Parquet file
data_path = 'gs://spotify-data-json/album_info_pq.json'
df = spark.read.json(data_path)
df.createOrReplaceTempView("album_info")

# Step 4: Create Table from the Temporary View (This creates a table in the metastore)
spark.sql("""
CREATE TABLE IF NOT EXISTS album_info
USING PARQUET
AS SELECT * FROM album_info;
""")
