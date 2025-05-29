from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Time start AND finish
# To create recommendations, I could create vectorDB of "song - artist" 

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

# PostgreSQL connection settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': DB_USER,
    'dbname': DB_NAME

}

def timestamp_valid(timestamp):
    """Check if a string is a valid ISO 8601 timestamp."""
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False


def get_top_artists(limit=10, timestamp = '2010-04-15T13:45:00Z'):
    """Search for top artists in the database."""
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        if not timestamp_valid:
            timestamp = '2010-04-15T13:45:00Z'

        print(timestamp)
        # Execute the query
        cursor.execute(
            """
            SELECT
                master_metadata_album_artist_name AS artist,
                SUM(ms_played) AS total_ms_played
            FROM songs_played
            WHERE 
                ts::timestamp >= %s AND
                master_metadata_album_artist_name IS NOT NULL
            GROUP BY master_metadata_album_artist_name
            ORDER BY total_ms_played DESC
            LIMIT %s;
            """,
            (timestamp, limit)
        )
        
        # Fetch and return the results
        results = cursor.fetchall()
        conn.close()

        return results

    except Exception as e:
        print(f"Error searching top artists: {e}")
        raise e 
    

def get_top_tracks(limit=100, timestamp = '2010-04-15T13:45:00Z'):
    """Return the most played tracks."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if not timestamp_valid:
            timestamp = '2010-04-15T13:45:00Z'


        print(timestamp)

        cursor.execute(
            """
            SELECT
                master_metadata_track_name AS track,
                master_metadata_album_artist_name AS artist,
                SUM(ms_played) AS total_ms_played
            FROM songs_played
            WHERE 
                ts::timestamp >= %s AND
                master_metadata_track_name IS NOT NULL
            GROUP BY master_metadata_track_name, master_metadata_album_artist_name
            ORDER BY total_ms_played DESC
            LIMIT %s;
            """,
            (timestamp, limit)
        )
        results = cursor.fetchall()
        conn.close()
        return results

    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        raise e
