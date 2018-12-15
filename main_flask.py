#to run:
#      main_flask.py run 
from main import classify
from flask import Flask, request, jsonify
app = Flask (__name__)


@app.route("/")
def index():
    return jsonify ({"result":"Welcome"}) #test

@app.route("/processPic/", methods=['GET','POST'])
def processPic():
    picbase64 = request.get_json()["picbase64"]
    commaIndex = picbase64.find(",")
    pic = picbase64[(commaIndex+1):]
    result = classify(pic)
    return result

if __name__ == "__main__":
    app.run(port=3001, debug=True)