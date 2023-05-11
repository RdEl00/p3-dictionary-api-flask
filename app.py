from flask import Flask, request, jsonify
from model.dbHandler import match_exact, match_like

app = Flask(__name__)

@app.get("/")
def index():
    """
    Default Route
    this method will
    1- Provide usage instructions formatted as JSON
    """
    response = {"usage": "/dict?=<word>"}
    return jsonify(response)

@app.get("/dict")
def dict():
    """
    Default Route
    this method will
    1- Accept a word from the request
    2- Try to find an exact match and return it if found
    3- If not found, find all approximate matches and return
    """
    words = request.args.getlist("word")

    if not words:
        response =  {"status":"error", "word" : words, "data": "Not a valid word or no word provided"}
        return jsonify(response)
    
    response = {"words" : []}
    
    for word in words:
        definitions = match_exact(word)
        if definitions:
            response["words"].append({ "status" : "success", "word":word ,"data": definitions})
        #return jsonify(response)

        definitions = match_like(word)
        if definitions:
            response["words"].append({"status":"partial","word":word ,"data": definitions})
            return jsonify(response)
        else:
            response["words"].append({"status":"error","word":word  ,"data": "word not found"})
    return jsonify(response)

if __name__ == "__main__":
    app.run()
