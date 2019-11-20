from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import summary_app

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/")
def hello():
    return "christ this iss annoying"


@app.route("/story_chars/", methods=['GET'])
@cross_origin(support_credentials=True)
def get_chars():
    tab_url = request.args.get("url")
    print(jsonify(summary_app.main_func(tab_url)))
    return jsonify(summary_app.main_func(tab_url))


if __name__ == "__main__":
    app.run(debug=True)
