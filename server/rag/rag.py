import os
import openai
import json
from dotenv import load_dotenv
from server.agents.spotify_agent import tools, function_registry
from server.logger.logger import vprint, bot_print, human_print
from server.db.db_search import find_unplayed_tracks


load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_agent_function(function_name, func_to_call, arguments):


    if func_to_call:
        return func_to_call(**arguments)  # <- Dynamic function call
    else:
        print(f"Unknown function: {function_name}")
        return None
    
def get_agent_function(response):
    func_call = response.output[0]

    vprint("func_call: ", func_call)
    if(func_call.type != 'function_call'):
        return None
    
    return func_call

def get_recommendations(func_to_call, arguments):
    data = func_to_call(**arguments)
    human_print(f"Data fed to get recommendations bot: {data}")
    song_recommendations = []
    previousMessages = [{
        "role": "system",
        "content": """You are a strict assistant that only generates track/artist combination that are real.
            Do not hallucinate or add any extra information."""
    }]
    iterations = 0
    while len(song_recommendations) < 10 and iterations < 10:
        iterations += 1
        prompt = f"""You are in charge finding at least 10 song recommendations based on a user's top songs: {data}
            Return your answer as a valid **JSON array** of tuples including (track name, artist name) — nothing else. 
            Example format: [["Track Name", "Artist Name"], ["another track name", "another artist name"]]
            """
        
        previousMessages.append({"role": "user", "content": prompt})
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=previousMessages,
            temperature=.1)
        
        response_content = response.choices[0].message.content
        # Add error handling if this does not work...
        try:
            track_artist_pairs = json.loads(response_content)
            if not isinstance(track_artist_pairs, list):
                raise ValueError("Expected a JSON array (list) as response.")
        except json.JSONDecodeError as e:
            print("JSON decoding failed:", e)
            print("Raw response content:", repr(response_content))
            track_artist_pairs = []  # fallback or trigger retry
        except Exception as e:
            print("Unexpected error:", e)
            track_artist_pairs = []

        song_recommendations.extend(find_unplayed_tracks(track_artist_pairs))
        vprint(f'Current Song Recommendation List: {song_recommendations}')
        
        
    bot_print(f"song_recommendations returned from recommendations bot: {response_content}")
    return response_content




def prompt_open_ai_generic(data, question):
    context = f"This is the data retreived for the user's query: {data}"

    prompt = f"""Based on the context of the user's data. {context}
    Generate a response to their question which was: {question}
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in music."},
            {"role": "user", "content": prompt}
        ],
        temperature=1
    )

    return response.choices[0].message.content

def prompt_open_ai_recommendations(recommendations, question):
    prompt = f"""Based on the users original question: {question}
    Please give them these recommendations {recommendations}
    Make sure to display this track name, not the track id    
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1
    )

    return response.choices[0].message.content

def ask_user_question(user_input):  
    response = openai.responses.create(
        model="gpt-4.1",
        input=[{"role": "user", "content": user_input}],
        tools=tools
    )

    func_call = get_agent_function(response)
    # Extract the function name and arguments from the user query.
    function_name = func_call.name
    arguments = json.loads(func_call.arguments)

    # Get the correct function to call from the registry
    func_to_call = function_registry.get(function_name)


    if function_name == "get_track_recommendations":
        recommendations =  get_recommendations(func_to_call, arguments)
        return prompt_open_ai_recommendations(recommendations, user_input)
    
    data = call_agent_function(function_name, func_to_call, arguments)

    if(data == None):
        print("Couldn't find a function that matched your question.")
        return "Sorry I couldn't find that. Try asking another question"

    open_ai_reply = prompt_open_ai_generic(data, user_input)

    print("Botify: ", open_ai_reply)
    print('-' * 75)
    return open_ai_reply