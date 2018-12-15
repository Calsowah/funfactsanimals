# Launches server on port 3001
# Command: main_flask.py run 
from main import classify
from flask import Flask, request, jsonify
app = Flask (__name__)

# Trivial route/"Home"
@app.route("/")
def index():
    return jsonify ({"result":"Welcome"}) #trivial

# Returns JSON object containing a field for the result of the neural net's prediction
# and a field for a fun fact. It achieves this by the following procedure:
# 1. Extracts base64 string representation of the uploaded image from the request object,
# 2. Removes metadata tags
# 3. invokes classify function from main on the resulting string
@app.route("/processPic/", methods=['GET','POST'])
def processPic():
    picbase64 = request.get_json()["picbase64"]
    commaIndex = picbase64.find(",")
    pic = picbase64[(commaIndex+1):]
    result = classify(pic)
    return result

if __name__ == "__main__":
    app.run(port=3001, debug=True)