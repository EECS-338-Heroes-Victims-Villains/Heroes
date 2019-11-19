from flask import Flask, request
import summary_app

app = Flask(__name__)


@app.route("/")
def hello():
    return "christ this iss annoying"


@app.route("/story_chars/<tab_url>", methods=['GET'])
def get_chars(tab_url=""):
    print(tab_url)
    print(summary_app.main_func(tab_url))
    return(tab_url)


if __name__ == "__main__":
    app.run(debug=True)
