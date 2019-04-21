from database import Db

class SuggestionApp:
    
    def __init__(self):
        self.db = Db()

    # Add the word to database, skip if it already exsists
    def addToDb(self, word, skip_if_exsists=True):
        words = self.tokenizeString(word)
        self.db.addList(words)
        return

    # tokenize the string
    # split on whitespaces. 
    # Also return the complete sentence except the last word as it might be incomplete
    # filter empty strings
    def tokenizeString(self, string):
        splitString = string.split()
        if(len(splitString) < 2): return []
        return filter(None, splitString + [" ".join(splitString[:-1])])

    # search for the word in db and return Suggestions
    # Add new words to DB
    def getSuggestions(self, query):
        # Add new words to DB
        self.addToDb(query)
        suggestions = self.db.getWordsByQuery(query)
        # get words from DB
        return suggestions

app = SuggestionApp()
print(app.getSuggestions("cri"))
