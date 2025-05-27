from flask import request,jsonify,render_template
from queries import execute_query
from translate import translateText
from model import model,tempfile

def setup_routes(app):
  
  @app.route("/", methods=["GET", "POST"])
  def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        q = request.get_json().get("q", "").strip()

        query = """
            SELECT * FROM language_code 
            WHERE language LIKE ? OR code LIKE ?
        """
        like_pattern = f"{q}%"
        results = execute_query(query, (like_pattern, like_pattern), fetch=True)

        return jsonify(results)
  
  @app.route("/translate_text",methods=["POST"])
  def translate():

        
    text = request.get_json().get("text")
    inp_code = request.get_json().get("inp_lang")
    out_code = request.get_json().get("out_lang")
    if not out_code:
       out_code = False

    translated = translateText(text,out_code,inp_code)


    return jsonify({"translated":translated.text})
  

  @app.route("/speech",methods=["GET"])
  def speech():
    if request.method == "GET":
      return render_template("speech.html")
    else:
      q = request.get_json().get("q", "").strip()

      query = """
            SELECT * FROM language_code 
            WHERE language LIKE ? OR code LIKE ?
        """
      like_pattern = f"{q}%"
      results = execute_query(query, (like_pattern, like_pattern), fetch=True)

      return jsonify(results)
    
  @app.route("/speech/translate",methods=["POST"])
  def speechTranslate():
    if "audio" not in request.files:
      print("error")
    else:
      audio_file = request.files["audio"]
      target_lang = request.form.get("target_lang")

      with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp:
        audio_path = temp.name
        audio_file.save(audio_path)


      result = model.transcribe(audio_path)
      transcript = result["text"]
      detected_lang = result["language"]


      result = translateText(transcript,target_lang)

      return jsonify({"transcript":transcript,"translation":result.text})
    
     
  
     
