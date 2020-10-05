"""
from koltk.corpus.nikl.json import 
"""

try: 
    import simplejson as json
except ImportError:
    import json

class Niklanson(dict):
    """
    NIKL Annotated Corpus JSON 
    """ 

    @classmethod
    def from_dict(cls, dic):
        if type(dic) is not dict:
            raise ValueError

        return cls(**dic)

    @classmethod
    def from_json(cls, json_str):
        return cls(**json.loads(json_str))

    def json(self):
        return json.dumps(self, ensure_ascii=False)



    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

class NiklansonList(list):
     def __init__(self, xlist):
        if type(xlist) is type(self):
            # TODO: implement clone
            raise Exception('not yet implemented!')
        elif type(xlist) is list:
            self.__init_from_json(xlist)

    
    
    


    
    
