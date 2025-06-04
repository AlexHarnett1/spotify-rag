from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from server.logger.logger import vprint

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

def send_sql_query(query, params):
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Execute the query
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
    
        return results
    
    except Exception as e:
        print(f"Error searching query: {e}")
        raise e 

def get_top_artists(limit=10, timestamp = '2010-04-15T13:45:00Z'):
    """Search for top artists in the database."""
    if not timestamp_valid:
        timestamp = '2010-04-15T13:45:00Z'

    vprint(f"Getting {limit} artists since {timestamp}")
    # Execute the query
    return send_sql_query(
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
    
def get_top_tracks(limit=25, timestamp = '2010-04-15T13:45:00Z'):
    """Return the most played tracks."""
    if not timestamp_valid:
        timestamp = '2010-04-15T13:45:00Z'


    vprint(f"Getting {limit} songs since {timestamp}")

    return send_sql_query(
        """
        SELECT
            spotify_track_uri AS uri,
            master_metadata_track_name AS track,
            master_metadata_album_artist_name AS artist,
            SUM(ms_played) AS total_ms_played
        FROM songs_played
        WHERE 
            ts::timestamp >= %s AND
            master_metadata_track_name IS NOT NULL
        GROUP BY 
            spotify_track_uri,
            master_metadata_track_name,
            master_metadata_album_artist_name
        ORDER BY total_ms_played DESC
        LIMIT %s;
        """,
        (timestamp, limit)
    )

def get_track_plays(track_name="", timestamp = '2010-04-15T13:45:00Z'):
    """Return how long the tracks been listened to/
    how many times the tracks been played."""

    if not timestamp_valid:
        timestamp = '2010-04-15T13:45:00Z'

    vprint(f"Getting plays of '{track_name}' since {timestamp}")

    return send_sql_query(
        """
        SELECT
            master_metadata_track_name AS track,
            master_metadata_album_artist_name AS artist,
            SUM(ms_played) AS total_ms_played
        FROM songs_played
        WHERE 
            ts::timestamp >= %s AND
            master_metadata_track_name = %s AND
            master_metadata_track_name IS NOT NULL
        GROUP BY master_metadata_track_name, master_metadata_album_artist_name;
        """,
        (timestamp, track_name)
    )