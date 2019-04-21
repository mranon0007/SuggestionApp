from database import Db

class SuggestionApp:
    
    # Add the word to database, skip if it already exsists
    def addToDb(self, word, skip_if_exsists=True):
        words = tokenizeString(word)
        return

    # tokenize the string
    def tokenizeString(self, string):
        return

    # search for the word in db and return Suggestions
    def getSuggestions(self, query):
        return