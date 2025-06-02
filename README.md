# Sbotify
This is a Retreival Augmented Genaration project using Open AI's API to make a chat bot that will generate a query to a database of spotify data and issue a response based on that data.

## Tech Stack

- **Frontend:** React + TypeScript + Axios
- **Backend:** Flask + Flask-Cors
- **Styling:** Custom CSS (Spotify-inspired)
- **API:** OpenAI

## Get the server running:
1. Navigate to server folder
2. Create a virtual environment
   - python3 -m venv venv
   - source venv/bin/activate
3. pip install -r requirements.txt
4. Create a .env file in the server folder
   - OPENAI_API_KEY=your_openai_key_here
   - DB_USER=your_db_username
   - DB_NAME=your_db_name
5. Create a postgres database
6. python3 db/db_setup.py
7. navigate to root folder and run: python3 -m server.main

## Get the client running:
1. Navigate to client/sbotify folder:
2. npm install
3. npm run dev
