for flask import *
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<h1>Hello World!</h1>"
  
  
def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
