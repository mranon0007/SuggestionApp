from pony import orm

db = orm.Database()

class WordsEng(db.Entity):
    word = orm.Required(str)

class WordsDutch(db.Entity):
    word = orm.Required(str)

class WordsGerman(db.Entity):
    word = orm.Required(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@orm.db_session
def addWord(word):
    return

@orm.db_session
def getWordsByQuery(query):
    return
