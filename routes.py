from flask import request,jsonify,render_template
from queries import execute_query

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
