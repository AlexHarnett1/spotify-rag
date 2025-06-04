from server.db.db_search import get_top_artists, get_top_tracks, get_track_plays
from datetime import datetime

now = datetime.now()

# Function registry (map of function names to callables)
function_registry = {
    "get_top_artists": get_top_artists,
    "get_top_tracks": get_top_tracks,
    "get_track_plays": get_track_plays,
    "get_track_recommendations": get_top_tracks
}

tools = [
{
    "type": "function",
    "name": "get_top_artists",
    "description": f"Get my top listened to artists. Today is {now}",
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of artists e.g. 25, 40"
            },
            "timestamp": {
                "type": "string",
                "description": "How long ago they'd like the data to go back. Return in timestamp form. Ex: 2010-04-15T13:45:00Z"
            }
        },
        "additionalProperties": False
    }
},
{
    "type": "function",
    "name": "get_top_tracks",
    "description": f"Get my top listened to tracks/songs. Today is {now}.",
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of tracks e.g. 25, 50"
            },
            "timestamp": {
                "type": "string",
                "description": "How long ago they'd like the data to go back. Return in timestamp form. Ex: 2010-04-15T13:45:00Z"
            }
        },
        "additionalProperties": False
    }
},
{
    "type": "function",
    "name": "get_track_plays",
    "description": f"Get the amount of time or number of times a track has been played. Today is {now}.",
    "parameters": {
        "type": "object",
        "properties": {
            "track_name": {
                "type": "string",
                "description": "Name of the track they want time played for."
            },
            "timestamp": {
                "type": "string",
                "description": "How long ago they'd like the data to go back. Return in timestamp form. Ex: 2010-04-15T13:45:00Z"
            }
        },
        "additionalProperties": False
    }
},
{
    "type": "function",
    "name": "get_track_recommendations",
    "description": f"Get track/song recommendations based on a given number of top tracks. Today is {now}.",
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of tracks e.g. 25, 50"
            },
            "timestamp": {
                "type": "string",
                "description": "How long ago they'd like the data to go back. Return in timestamp form. Ex: 2010-04-15T13:45:00Z"
            }
        },
        "additionalProperties": False
    }
}]
