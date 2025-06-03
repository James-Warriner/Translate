from flask import Response, redirect, request,jsonify,render_template,session
from image_processing import get_image, preProcessImage
from queries import execute_query,getUser,textTranslateUpload,fetchRecents,speechTranslateUpload
from translate import translateText
from model import model,tempfile
from session_handler import assignTemp, isLoggedIn,register,login,authenticateCode
from helpers import returnError

def setup_routes(app):

  @app.before_request
  def ensure_temp_id():
    assignTemp()


  @app.route("/register",methods = ["GET","POST"])
  def registerRoute():
    return register(request)
  
  @app.route("/auth", methods=["GET", "POST"])
  def auth():



    returnVal = authenticateCode(request)
    if returnVal == "GET":
      html = render_template("authRegister.html")
      return html
    else:
      print(returnVal)
      return returnVal
  
  @app.route("/login",methods = ["GET","POST"])
  def loginRoute():
    return login(request)
  
  @app.route("/logout",methods=["GET"])
  def logout():
    session.clear()
    return redirect("/")


  
  @app.route("/", methods=["GET", "POST"])
  
  
  def home():
    assignTemp()
    print(session["temp_id"])
    if request.method == "GET":
        print(isLoggedIn())
        return render_template("index.html", isLoggedIn=isLoggedIn(),user=getUser() )
    else:
        q = request.get_json().get("q", "").strip()

        query = """
            SELECT * FROM language_code 
            WHERE language LIKE ? OR code LIKE ?
        """
        like_pattern = f"{q}%"
        results = execute_query(query, (like_pattern, like_pattern), fetch=True)

        return jsonify({"results":results})
  
  @app.route("/translate_text",methods=["POST"])
  def translate():

        
    text = request.get_json().get("text")
    inp_code = request.get_json().get("inp_lang")
    out_code = request.get_json().get("out_lang")
    inp_id = request.get_json().get("inp_lang_id")
    out_id = request.get_json().get("out_lang_id")
    if not out_code:
       out_code = False

    translated = translateText(text,out_code,inp_code)

    if isLoggedIn():
      completed = textTranslateUpload(text,translated.text,inp_id,out_id)

      if not completed:
        print("error")





    return jsonify({"translated":translated.text})
  

  @app.route("/speech",methods=["GET"])
  def speech():
    if request.method == "GET":
      return render_template("speech.html",isLoggedIn=isLoggedIn(),user=getUser())
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

      rows = execute_query("SELECT id FROM language_code WHERE code = ?",(target_lang.lower(),),fetch=True)
      if not isinstance(rows, list) or not rows:
        return returnError("Unknown target language", 400)
      target_id = rows[0]["id"]

      print(detected_lang)

      
      rows2 = execute_query("SELECT id FROM language_code WHERE code = ?",(detected_lang.lower(),),fetch=True)
      if not isinstance(rows2, list) or not rows2:
        return returnError("Unknown detected language", 400)
      source_id = rows2[0]["id"]



      result = translateText(transcript,target_lang)

      with open(audio_path, "rb") as f:
        audio_blob = f.read()


      speechTranslateUpload(audio_blob,transcript,result.text,source_id,target_id)

      return jsonify({"transcript":transcript,"translation":result.text})
    

  @app.route("/recents",methods=["GET"])
  def getRecents():
    results = fetchRecents()
    

    if not results:
      return jsonify({})
      

    return jsonify({"results":results})
  

  @app.route("/user_status",methods=["GET"])
  def getStatus():
    if session.get("user_id") is not None:
      return jsonify({"status":"true"})
    
    return jsonify({"status":"false"})
    



  
  @app.route("/translation/<int:trans_id>",methods=["GET"])
  def translation_details(trans_id):
    if session.get("user_id") is None:
      return redirect("/login")
    
    rows = execute_query(
        "SELECT t.*, "
        "src.code AS input_code, src.language AS input_language, "
        "tgt.code AS output_code, tgt.language AS output_language "
        "FROM translation t "
        "JOIN language_code src ON t.source_lang_id = src.id "
        "JOIN language_code tgt ON t.target_lang_id = tgt.id "
        "WHERE t.id = ? AND t.user_id = ?",
        (trans_id, session["user_id"]),
        fetch=True
    )

    if not rows:
      return redirect("/home")
    
    if rows[0]["type"] == "text":
    
      return render_template("viewText.html", recent=rows[0],isLoggedIn=isLoggedIn(),user=getUser())
    
    return render_template("viewSpeech.html",recent=rows[0],isLoggedIn=isLoggedIn(),user=getUser())
    
  @app.route("/translation/<int:trans_id>/audio",methods=["GET"])
  def translation_audio(trans_id):
    if session.get("user_id") is None:
      return returnError("Error")
    else:
      rows = execute_query("SELECT original_audio, user_id FROM translation WHERE id= ?",(trans_id,),fetch=True)

      row = rows[0]

      if row["user_id"] != session["user_id"]:
        return returnError("Error")
      
      blob = row["original_audio"]
      if blob is None:
        return returnError("error")
      
      return Response(blob,mimetype="audio/webm",headers={"Content-Length":str(len(blob))})


  @app.route("/image",methods=["GET","POST"])
  def translateImage():
    if request.method == "GET":
      return render_template("uploadImage.html")
    
    
    src_code = request.form.get("src_code")
    trgt_code = request.form.get("trgt_code")
    
    image = get_image(request)

    text = preProcessImage(image,src_code)

    translatedText = translateText(text,trgt_code,source_lang=src_code)

    return jsonify({"translated":translatedText.text,"text":text})
    
  
     
