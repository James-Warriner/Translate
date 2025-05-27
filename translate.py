import os
from dotenv import load_dotenv
import deepl


def initDL():
  load_dotenv()
  key = os.getenv("DEEPL_API_KEY")
  print(key)
  return key

def translateText(text,target_lang, source_lang=False):
  print(target_lang)
  print(source_lang)
  key = initDL()
  translator = deepl.DeepLClient(key)

  target_lang = target_lang.upper()
  if target_lang == "EN":
      target_lang = "EN-US"
  

  if source_lang:
    source_lang = source_lang.upper()
    
    print(source_lang)
    result = translator.translate_text(text,source_lang=source_lang, target_lang=target_lang)
    
    

  else:
    result = translator.translate_text(text, target_lang=target_lang)

 
 

  print(result)

  return result


