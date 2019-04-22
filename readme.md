# Intech Test
This is a simple system to autocomplete words and sentences.  

The App can be used throught the SuggestionApp python class, WebSocket API or a web based front-end app.    

SQLite database was used for storage purpose.

# Installation

#### Requirements

- Python 2.7 with Pip
- Chrome 16 + or a browser with WebSockets support (**Edge** Not Supported) [Only required if using the front-end web app]

#### Installation

- `git clone https://github.com/mranon0007/SuggestionApp  `
- `pip install -r requirments.txt`

# Usage

Make sure port `13254` is free.

## Quick Run

- Run the WebSocket Server: `python Api.py`
- Running the Flask WebApp:
  
  On Linux      : `export FLASK_APP=WebApp.py`  
  On Windows CMD: `set FLASK_APP=WebApp.py`  
  On PowerShell : `$env:FLASK_APP = "WebApp.py"`

- `flask run`
  
  You can now access the App on `http://127.0.0.1:5000/`

In case you want to build a custom frontend, read below.

## SuggestionApp
The base class which communicates with the database and contain the autocompletion logic.

### Methods

| Method                   | Description                                                 | Takes           | Gives |
|--------------------------|-------------------------------------------------------------|-----------------|-------|
| `getSuggestions()`       | Returns a list of suggestions. Add word to db if not exsists.| word, lang(str, optional), count(int, optional)        | List of (id, string)  |

## WebSocketApi

The websocket server can be started with `python Api.py`. The endpoint `ex: http://127.0.0.1:13254` accepts a json encoded dict with format 
```
{
    "msg_id": "str", //str = message identifier
    "type": "autocomplete", //message type, no other types accepted.
    "data": {
        "query": "str", //search query
        "lang" : "str", //one of the following [ "Eng", "Dutch", "German" ]
        "limit": int //Count of Suggestions to return
    }
}
```
The Api returns a json encoded list of tuples(id, suggestion).

## Front-end Flask Web App

To run the WebApp, you need to set the environment variable `FLASK_APP=WebApp.py`. Run one of the followin:

On Linux      : `export FLASK_APP=WebApp.py`  
On Windows CMD: `set FLASK_APP=WebApp.py`  
On PowerShell : `$env:FLASK_APP = "WebApp.py"`

To launch the WebServer, run `flask run`

# Folder Structure

```bash
app
├── resources               # App resources
│   └── wordsDutch.txt      # default Dutch Dict
│   └── wordsEng.txt        # default Eng Dict
│   └── wordsGerman.txt     # default German Dict
├── static                  # Static Files for Flask
├── Api.py                  # WebSocket Server
├── database.py             # Database
├── readme.md               # 
├── requirments.txt         # python/pip requirments
├── SuggestionApp.py        # Base App
├── WebApp.py               # Flask App
```

# FAQs

#### How is the database designed? 

We have 3 tables for 3 languages; English, Duthc & German.
We can have 1 table for words with an additional column indicating the language but we'll have to use the 'where' sql clause in every select query which consumes extra processing resources.
