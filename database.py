from pony import orm
import sys
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

        db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
        db.generate_mapping(create_tables=True)

    @orm.db_session
    def addWord(self, word, lang="Eng"):
        dictName = deepgetattr(getattr(sys.modules[__name__], self.__class__.__name__), 'Words'+lang)
        word     = dictName(word=word)
        db.commit()
        return

    @orm.db_session
    def getWordsByQuery(self, query):
        return

    # Models - Each class represents 1 Table(or a dictionary of different languages)
    class WordsEng(db.Entity):
        word = orm.Required(str)

    class WordsDutch(db.Entity):
        word = orm.Required(str)

    class WordsGerman(db.Entity):
        word = orm.Required(str)

