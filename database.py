from pony import orm
import sys
import os
import codecs

db = orm.Database()

def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    # https://pingfive.typepad.com/blog/2010/04/deep-getattr-python-function.html
    return reduce(getattr, attr.split('.'), obj)

class Singleton(object):
    _instance    = None
    _initialized = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class Db(Singleton):

    def __init__(self):
        if(self._initialized): return
        else: self._initialized = True

        # Add data to database from resources folder!
        dbexsists = os.path.isfile('database.sqlite')
        if not dbexsists:

            # if dictionaries don't exsists in resources folder.
            if (not (os.path.isfile('resources/wordsEng.txt')) 
                or not (os.path.isfile('resources/wordsDutch.txt')) 
                or not (os.path.isfile('resources/wordsGerman.txt'))
                ):
                raise Exception("Dict not exsist in Resources Folder")
            
            try:
                db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
                db.generate_mapping(create_tables=True)

                print("Generating Database. It can take a few minutes as the data is around 20 Mb")
                with codecs.open("resources/wordsEng.txt", 'r', encoding='utf-8', errors='ignore') as outfile:
                    lines = outfile.read().splitlines()
                    self.addList(lines, check_for_duplicates = False)

                with codecs.open("resources/wordsDutch.txt", 'r', encoding='utf-8', errors='ignore') as outfile:
                    lines = outfile.read().splitlines()
                    self.addList(lines, lang="Dutch", check_for_duplicates = False)

                with codecs.open("resources/wordsGerman.txt", 'r', encoding='utf-8', errors='ignore') as outfile:
                    lines = outfile.read().splitlines()
                    self.addList(lines, lang="German", check_for_duplicates = False)

                print("Generated Database Completely.")
            except:
                os.remove("database.sqlite")
                raise Exception("Problem in generating the Db")

        else:
            db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
            db.generate_mapping(create_tables=True)
            # orm.set_sql_debug(True)

    @orm.db_session
    def addWord(self, word, lang="Eng"):
        dictName = deepgetattr(getattr(sys.modules[__name__], self.__class__.__name__), 'Words'+lang)
        word     = dictName(word=word)
        try:
            db.commit()
        except: 
            pass
        return

    @orm.db_session
    def addList(self, words, lang="Eng", check_for_duplicates=True):
        words = set(filter(None, words))

        # filter empty & duplicate words 
        dictName = deepgetattr(getattr(sys.modules[__name__], self.__class__.__name__), 'Words'+lang)

        # remove words already in db
        if check_for_duplicates:
            queryResult = set(orm.select(c.word for c in dictName if( c.word in words) )[:])
            words       = words - (words & queryResult)

        for word in words:
            word_ = dictName(word=word)
        
        # commiting only once rather than committing for every word
        db.commit()
        return

    @orm.db_session
    # returns [ (id,word),... ]
    def getWordsByQuery(self, query, lang="Eng", limit=10):
        if not query: return []
        limit       = int(limit)
        dictName    = deepgetattr(getattr(sys.modules[__name__], self.__class__.__name__), 'Words'+lang)
        queryResult = orm.select((c.id, c.word) for c in dictName if(c.word.startswith(query)) )[:limit]
        return queryResult

    '''
    Models - Each class represents 1 Table (or a dictionary of different languages) 
    Naming Convention For Dictionary: "Words"+Language
    
    We have 3 tables for 3 languages; English, Duthc & German.
    We can have 1 table for words with an additional column indicating the 
    language but we'll have to use the 'where' sql clause in every select query which consumes extra processing resources.
    '''
    
    class WordsEng(db.Entity):
        word = orm.Required(str, unique=True)

    class WordsDutch(db.Entity):
        word = orm.Required(str, unique=True)

    class WordsGerman(db.Entity):
        word = orm.Required(str, unique=True)

