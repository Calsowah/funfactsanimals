# from main import classify //having errors with importing other libraries from main
from flask import Flask
app = Flask (__name__)


@app.route("/")
def index():
    return "Welcome"

@app.route("/processPic/<pic>")
def processPic(pic):
    # result = classify(pic)
    return "done" #should be return result 

if __name__ == "__main__":
    app.run(debug=True)