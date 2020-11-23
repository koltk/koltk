r"""NIKL ANnotated Corpus JSON (Niklanson) Objects

.. code-block::

  Corpus
    CorpusMetadata
    DocumentList
      Document
        DocumentMetadata
        SentenceList
          Sentence
            WordList, Word
            MorphemeList, Morpheme
            WSDList, WSD
            NEList, NE
            DPList, DP
            SRLList, SR
        ZAList, ZA
        CRList, CR



"""


from __future__ import annotations
from .base import Niklanson, NiklansonList
import re
import json

class CorpusMetadata(Niklanson):
    def __init__(self, title = None,
                 creator = None,
                 distributor = None,
                 year = None,
                 category = None,
                 annotation_level = [],
                 sampling = None,
                 **kwargs):
        self.title = title
        self.creator = creator
        self.distributor = distributor
        self.year = year
        self.category = category
        self.annotation_level = annotation_level
        self.sampling = sampling
        self.update(kwargs)
    
class Corpus(Niklanson):
    """Corpus: the top level object.

    - id
    - :class:`.CorpusMetadata`
    - :class:`.DocumentList`

    JSON:
    
    .. code-block:: json
      
      {
        "id" : "",
        "metadata" : {},
        "document" : []
      }
    
    Args:
        corpus (Corpus) : corpus
    

    Example:
    
    .. code-block:: python

        Corpus()
        Corpus(id=None, metadata=None, document=[])

    """
    def __init__(self,
                 id: str = None,
                 metadata : {} = {},
                 document: [] = [],
                 **kwargs):
        self.id = id
        self.metadata = CorpusMetadata(**metadata)
        self.document = DocumentList(document)
        self.update(kwargs)

    @classmethod
    def strict(cls, id, metadata, document):
        return cls(id, metadata, document)
        
    @property
    def document_list(self):
        """ :class:`.DocumentList`
        """
        #if self.document_list is None:
        #    self.__document_list = DocumentList(self.__json['document'])

        return self.document

    def __repr__(self):
        return 'Corpus(id={})'.format(self.id)

class DocumentMetadata(Niklanson):
    def __init__(self,
                 title : str = None,
                 author : str = None,
                 publisher : str = None,
                 date : str = None,
                 topic : str = None,
                 url : str = None,
                 **kwargs):
        self.title = title 
        self.author = author
        self.publisher = publisher
        self.date = date
        self.topic = topic
        self.url = url
        self.update(kwargs)

    @classmethod
    def strict(title, author, publisher, date, topic, url):
        return cls(title, author, publisher, date, topic, url)
    
class Document(Niklanson):
    """
    Document()

    ::

        >>> d = Document(id='X200818')
      
    """
    def __init__(self,
                 id = None,
                 metadata = {},
                 sentence = [],
                 CR = [],
                 ZA = [],
                 **kwargs):
        self.id = id
        self.metadata = DocumentMetadata.from_dict(metadata)
        self.sentence = SentenceList(sentence, parent=self)
        self.CR = CRList(CR)
        self.ZA = ZAList(ZA)
        self.update(kwargs)

    @classmethod
    def strict(cls, id=None, metadata={}, sentence = [], CR = [], ZA = []):
        return cls(id, metadata, sentence, CR, ZA)

    @property
    def sentence_list(self):
        return self.sentence
        
    @property
    def za_list(self):
        return self.ZA
  
    @property
    def cr_list(self):
        return self.CR
  
    def __repr__(self):
        return 'Document(id={})'.format(self.id)
    
    def __str__(self):
        return json.dumps(self, ensure_ascii=False)

    def getSentenceById(self, sentence_id):
        if not hasattr(self, '__sentence_id2index'):
            self.__sentence_id2index = {}
            for i, sent in enumerate(self.sentence_list):
                self.__sentence_id2index[sent.id] = i
                
        return self.sentence_list[self.__sentence_id2index[sentence_id]]

 
class DocumentList(NiklansonList):
    element_type = Document
    
   
class Sentence(Niklanson):
    """
    Sentence(id, form)

    ::

        >>> s = Sentence('X200818', '아이들이 책을 읽는다.')
   """
    def __init__(self,
                 parent: Document = None,
                 id: str = None,
                 form: str = None,
                 **kwargs):
        
        self.__parent = parent
        self.id = id
        self.form = form
        for name, value in kwargs.items():
            if name == 'word' : self.word = WordList(value, parent=self)
            elif name == 'morpheme' : self.morpheme = MorphemeList(value)
            elif name == 'WSD' : self.WSD = WSDList(value)
            elif name == 'NE' : self.NE = NEList(value)
            elif name == 'DP' : self.DP = DPList(value)
            elif name == 'SRL' : self.SRL = SRLList(value)
            else: setattr(self, name, value)

    @classmethod
    def strict(cls, id, form, word, morpheme, WSD, NE, DP, SRL):
        return cls(id, form, word, morpheme, WSD, NE, DP, SRL)

    @property
    def parent(self):
        return self.__parent

    @property
    def word_list(self):
        if not hasattr(self, 'word'):
            self.word = []
            b = 0
            for i, wform in enumerate(self.form.split()):
                e = b + len(wform)
                self.word.append(Word(id=i + 1, form=wform, begin=b, end=e))
                b = e + 1

        return self.word
    
    @property
    def morpheme_list(self):
        return self.morpheme
    
    @property
    def wsd_list(self):
        return self.WSD
        
    @property
    def ne_list(self):
        return self.NE
  
    @property
    def dp_list(self):
        return self.DP
  
    @property
    def srl_list(self):
        return self.SRL
  
    def __init_word_list_from_sentence_form(self):
        self.__word_list = []
        beg = 0
        i = 0
       
        for tok in re.split('(\s+)', self.form):
            if tok == '' : continue
            elif re.match('\s', tok[0]) : beg += len(tok)
            else:
                i += 1
                self.word.append(Word(i, tok, beg, beg + len(tok))) 
                beg += len(tok)
                
    @property
    def fwid(self):
        toks = self.id.split(".")
        if len(toks) == 2:
            docid, sentnum = toks
            fw_sid = "{}-{:04d}-{:05d}-{:05d}".format(docid, 1, 1, int(sentnum))
        elif len(toks) == 4:
            corpusid, docnum, paranum, sentnum = toks
            fw_sid = "{}-{:04d}-{:05d}-{:05d}".format(corpusid, int(docnum), int(paranum), int(sentnum))
        else:
            sys.exit(sid)

        return fw_sid


    @property
    def dsid(self):
        """dsid: document sentence id.
        within a document
        """
        return self.__dsid


    @dsid.setter
    def dsid(self, value):
        self.__dsid = value
    
    


    def __repr__(self):
        return 'Sentence(id={}, form={})'.format(self.id, self.form)
        

    def wordAt(self, charind):
        if not hasattr(self, '__charind2wordid'):
            self.__charind2wordid = [None] * len(self.form) 
            for i, w in enumerate(self.word_list):
                self.__charind2wordid[w.slice] = [w.id] * len(w.form)

        try:
            return self.word_list[self.__charind2wordid[charind] - 1]
        except:
            raise Exception('No word at {}: {}'.format(charind, self.form))

class SentenceList(NiklansonList):
    element_type = Sentence


    def postprocess(self):
        for i, sentence in enumerate(self):
            sentence.dsid = 's{}'.format(i+1)
    
            
class Word(Niklanson):
    """
    Word
    """
    def __init__(self,
                 parent: Sentence = None,
                 id : int = None,
                 form : str = None,
                 begin : int = None,
                 end : int = None,
                 **kwargs):
        self.__parent = parent
        self.id = id
        self.form = form
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, id: int, form: str, begin: int, end: int):
        return cls(id, form, begin, end)

    @property
    def parent(self):
        return self.__parent
    
    @property
    def gid(self):
        return '{}_{:03d}'.format(self.__parent.fwid, self.id)

    @property
    def dswid(self):
        return '{}_{}'.format(self.__parent.dsid, self.id)
    
    @property
    def slice(self):
        return slice(self.begin, self.end) 

    @property
    def slice_str(self):
       return '{}:{}'.format(self.begin, self.end) 

class WordList(NiklansonList):
    element_type = Word

   

class Morpheme(Niklanson):
    """Morpheme
    """
    def __init__(self,
                 id : int = None,
                 form: str = None,
                 label : str = None,
                 word_id : int = None,
                 position : int = None,
                 **kwargs):
        self.id = id
        self.form = form
        self.label = label
        self.word_id = word_id
        self.position = position
        self.update(kwargs)
        self.__str = None

    @classmethod
    def strict(cls, id, form, label, word_id, position):
        return cls(id, form, label, word_id, position)

    @property
    def str(self):
        if self.__str is None:
            self.__str = self.form + '/' + self.label

        return self.__str

class MorphemeList(NiklansonList):
   element_type = Morpheme 
 

class WSD(Niklanson):
    """
    WSD (Word Sense Disambiguation)
    """
    def __init__(self,
                 word: str = None,
                 sense_id: int = None,
                 pos : str = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        self.word = word
        self.sense_id = sense_id
        self.pos = pos
        self.begin = begin
        self.end = end
        self.update(kwargs)
        
    @property
    def str(self):
        return '{}__{:03d}/{}'.format(self.word, self.sense_id, self.pos)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)
    
class WSDList(NiklansonList):
    element_type = WSD
       

class NE(Niklanson):
    """
    NE (Named Entity)
    """
    def __init__(self,
                 id: int = None,
                 form: str = None,
                 label: str = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        self.id = id
        self.form = form
        self.label = label
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, id, form, label, begin, end):
        return cls(id, form, label, begin, end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def str(self):
        return '{}/{}'.format(self.form, self.label)
    
class NEList(NiklansonList):
    element_type = NE



class DP(Niklanson):
    """
    DP (Denpendency Parsing)
    """
    def __init__(self,
                 word_id: int = None,
                 word_form: str = None,
                 head: int = None,
                 label: str = None,
                 dependent: list[int] = None,
                 **kwargs):
        self.word_id = word_id
        self.word_form = word_form
        self.head = head
        self.label = label
        self.dependent = dependent
        self.update(kwargs)
        
class DPList(NiklansonList):
    element_type = DP

    @property
    def root_word_id(self) :
        for dp in self:
            if dp.head == -1:
                return dp.word_id

    @property
    def heads(self):
        if not hasattr(self, '_heads'):
            self._heads = []
            for dp in self:
                self._heads.append(dp.head)

        return self._heads
      
class SRLPredicate(Niklanson):
    def __init__(self,
                 form: str = None,
                 begin: int = None,
                 end: int = None,
                 lemma: str = None,
                 sense_id: int = None,
                 **kwargs):
        self.form = form
        self.begin = begin
        self.end = end
        self.lemma = lemma
        self.sense_id = sense_id
        self.update(kwargs)

    @classmethod
    def strict(cls, form: str, begin: int, end: int, lemma: str, sense_id: int):
        return cls(form, begin, end, lemma, sense_id) 

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)

    @property
    def str(self):
        return self.__str__()
    
    def __str__(self):
        return '{}__{}'.format(self.lemma, self.sense_id)

class SRLArgument(Niklanson):

    def __init__(self,
                 form: str = None,
                 label: str = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        self.form = form
        self.label = label
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, form: str, label: str, begin: int, end: int):
        return cls(form, label, begin, end)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)

    @property
    def str(self):
        return '{}/{}'.format(self.form.split()[-1], self.label)



class SRLArgumentList(NiklansonList):
    element_type = SRLArgument

class SRL(Niklanson):
    """
    SRL (Semantic Role Labeling)
    
    consists of a predicate and a list of arguments::
    
        >>> SRL()
        >>> SRL(predicate={}, argument=[{}, {}])
    """
    def __init__(self,
                 predicate: {} = {},
                 argument: [] = [],
                 **kwargs):
        self.predicate = SRLPredicate(**predicate)
        self.argument_list = SRLArgumentList(argument)
        self.update(kwargs)
        
    @classmethod
    def strict(cls, predicate: {}, argument: []):
        """
        """
        return cls(predicate, argument)
    
class SRLList(NiklansonList):
    element_type = SRL
    
    
class CRMention(Niklanson):
    def __init__(self,
                 form : str = None,
                 sentence_id : str = None,
                 begin : int = None,
                 end : int = None,
                 NE_id : int = None,
                 **kwargs):
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        self.NE_id = NE_id
        self.update(kwargs)

    @classmethod
    def strict(cls, form: str, sentence_id: str, being: int, end: int, NE_id : int):
        return cls(form, sentence_id, begin, end, NE_id)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)

class CRMentionList(NiklansonList):
    element_type = CRMention
    
class CR(Niklanson):
    """
    CR (Cross Reference)
    
    mention: list of mentions
    """
    def __init__(self, mention: [] = [], **kwargs):
        """
        """
        self.mention = CRMentionList(mention)
        self.update(kwargs)

    @classmethod
    def strict(cls, mention: []):
        return cls(mention)

    @property
    def mention_list(self):
        return self.mention
 
class CRList(NiklansonList):
    element_type = CR

class ZAPredicate(Niklanson):
    def __init__(self,
                 form: str = None,
                 sentence_id: int = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        self.update(kwargs)

    @classmethod
    def strict(cls, form, sentence_id, begin, end):
        return cls(form, sentence_id, begin, end)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)

class ZAAntecedent(Niklanson):
    def __init__(self,
                 form: str = None,
                 type: str = None,
                 sentence_id: int = None,
                 begin: int = None,
                 end: int = None,
                 **kwargs):
        self.type = type
        self.form = form
        self.sentence_id = sentence_id
        self.begin = begin
        self.end = end
        self.update(kwargs)
        
    @classmethod
    def strict(cls, form, type, sentence_id, begin, end):
        return cls(form, type, sentence_id, begin, end)

    @property
    def slice(self):
        return slice(self.begin, self.end)

    @property
    def slice_str(self):
        return '{}:{}'.format(self.begin, self.end)

class ZAAntencedentList(NiklansonList):
    element_type = ZAAntecedent
        
class ZA(Niklanson):
    def __init__(self,
                 predicate: {} = {},
                 antecedent: [] = [],
                 **kwargs):
       self.predicate = ZAPredicate(**predicate)
       self.antecedent = ZAAntencedentList(antecedent)

    @classmethod
    def strict(predicate: {}, antecedent: []):
        return cls(predicate, antecedent)
   
class ZAList(NiklansonList):
    element_type = ZA
