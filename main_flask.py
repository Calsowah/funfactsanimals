#to run:
#      main_flask.py run 
# from main import classify //having errors with importing other libraries from main
import funFactScraper 
from main import classify
from flask import Flask
app = Flask (__name__)


@app.route("/")
def index():
    return "Welcome" #test

@app.route("/processPic/<pic>")
def processPic(pic):
    result = classify(pic)
    # scrape using result
    return result #should be return json with fields result and fun 

if __name__ == "__main__":
    app.run(debug=True)