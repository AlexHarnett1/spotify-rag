import psycopg2
from psycopg2.extras import RealDictCursor


DATABASE_NAME="spotify_data"

# PostgreSQL connection settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': DATABASE_NAME,
    'user': 'alexharnett'
}

def get_top_artists(limit=10):
    """Search for top artists in the database."""
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Execute the query
        cursor.execute(
            """
            SELECT
                master_metadata_album_artist_name AS artist,
                SUM(ms_played) AS total_ms_played
            FROM songs_played
            WHERE master_metadata_album_artist_name IS NOT NULL
            GROUP BY master_metadata_album_artist_name
            ORDER BY total_ms_played DESC
            LIMIT %s;
            """,
            (limit,)
        )
        
        # Fetch and return the results
        results = cursor.fetchall()
        conn.close()

        return results

    except Exception as e:
        print(f"Error searching activities: {e}")
        raise e 

# print(get_top_artists(10))
        