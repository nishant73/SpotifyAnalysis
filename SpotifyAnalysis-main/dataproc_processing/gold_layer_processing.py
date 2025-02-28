# Step 1: Create gold layer DB
spark.sql("""
CREATE DATABASE IF NOT EXISTS spotify_gold_db 
LOCATION 'gs://spotify-etl-gold/artist_bronze.db';
""")

# Step 2: Use the Database (Set the current database context)
spark.sql("USE spotify_gold_db ;")


# Step 3: Create the table if it doesn't exist
spark.sql("""
CREATE TABLE IF NOT EXISTS spotify_track_info (
    name STRING,
    id STRING,
    artist_id STRING,
    href STRING,
    release_date STRING,
    uri STRING,
    artist_name STRING
) USING PARQUET;
""")

# Step 4: Insert data into the table
spark.sql("""
INSERT INTO spotify_track_info
SELECT 
    al.name,
    al.id,
    al.artist_id,
    al.href,
    al.release_date,
    al.uri,
    ar.name AS artist_name 
FROM 
    album_bronze_db.album_info al 
INNER JOIN 
    artist_bronze_db.artist_info ar
ON 
    al.artist_id = ar.id;
""")