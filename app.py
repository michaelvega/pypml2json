import json
import os
from bs2json import bs2json
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_cors import CORS


def remove_duplicates(og_list: list) -> list:
    res = []
    [res.append(x) for x in og_list if x not in res]
    return res


def opml2json(opml_string):
    soup = BeautifulSoup(opml_string, features='html.parser')  # html.parser worked best during development as
    # opposed to lxml

    converter = bs2json()

    child_elements = []

    for child in soup.recursiveChildGenerator():
        if child.name:
            child_elements.append(str(child.name))
            # print(child.name)

    print("child elements: ")
    child_elements_no_dupes = remove_duplicates(child_elements)
    print(str(child_elements_no_dupes))

    if "outline" in child_elements:
        tags = soup.findAll('outline')
        json_list = converter.convertAll(tags)
        json_dict = json_list[0]

        json_object = json.dumps(json_dict, indent=4)  # Upside Down
        print(json_object)
        return json_dict
    else:
        return False


app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
@app.route('/API')
@app.route('/API/')
def home():
    return render_template('index.html')


@app.route("/API/opml2json/form", methods=["POST", "GET"])
def form():
    empty_dict = {"results": "Unable to Read"}
    if request.method == "POST":
        opml = str(request.form["nm"])
        res_json = opml2json(opml)
        if res_json:
            return res_json
        else:
            return empty_dict
    else:
        return render_template("form.html")


@app.route("/API/opml2json", methods=["POST"])
@app.route("/API/opml2json/", methods=["POST"])
def converter_post():
    empty_dict = {"results": "Unable to Read"}
    Query = str(request.data)
    Query = Query.replace("\\n", "")
    Query = Query.replace("\\r", "")
    Query = Query.replace("\\t", "")
    res_json = opml2json(Query)
    if res_json:
        return res_json
    else:
        return empty_dict


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))  # should be 0.0.0.0 and 8080
