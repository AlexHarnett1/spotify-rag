from db_search import get_top_artists, get_top_tracks

# Function registry (map of function names to callables)
function_registry = {
    "get_top_artists": get_top_artists,
    "get_top_tracks": get_top_tracks
}

tools = [
{
    "type": "function",
    "name": "get_top_artists",
    "description": "Get my top listened to artists. Today is May 30, 2025.",
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
    "description": "Get my top listened to tracks/songs. Today is May 30, 2025.",
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
