import warnings
warnings.simplefilter('ignore')
from janome.tokenizer import Tokenizer
from gensim.models import KeyedVectors

#load_model
model_dir = './entity_vector.model.bin'
model = KeyedVectors.load_word2vec_format(model_dir, binary=True)

#search_similar_word
def similar_word(text):
  tokens =j_t.tokenize(text)
  result = ''
  naoya = []

  for token in tokens:
      # 品詞を取り出し
      partOfSpeech = token.part_of_speech.split(',')[0]
      if partOfSpeech == u'名詞':
          result += token.surface
      else: 
        try:
          for i in range(3):
            res = model.most_similar('['+result+']')[i]
            res1 = res[0].split(',')[0]
            naoya.append(res1)
          
                  
          result = ''
        except KeyError as error:
          result = ''
  return naoya
