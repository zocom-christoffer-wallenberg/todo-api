from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

items = [
    { "todo": 'Köp kaffe', "id": str(uuid4()), "done": False },
    { "todo": 'Köp kaka', "id": str(uuid4()), "done": False },
    { "todo": 'Brygg kaffe', "id": str(uuid4()), "done": False },
    { "todo": 'Drick kaffe', "id": str(uuid4()), "done": False }
]

@app.route("/api/todo", methods=["GET", "POST"])
def getItems():
    if request.method == "GET":
        return jsonify({ "success": True, "items": items })
    elif request.method == "POST":
        body = request.get_json(silent=True)

        if body != None and body.get("todo") != None:
            body = request.json["todo"]

            item = {
                "todo": body,
                "id": str(uuid4()),
                "done": False
            }

            items.append(item)

            return jsonify({ "success": True })
        else:
            return jsonify({ "success": False })

@app.route("/api/todo/<id>", methods=["PUT", "DELETE"])
def updateTodos(id):
    if request.method == "PUT":

        idExist = False

        for item in items:
            if item.get("id") == id:
                idExist = True
        
        if idExist == True:
            body = request.get_json(silent=True)

            if body != None and body.get("todo") != None or body.get("done") != None:
                for index, todo in enumerate(items):
                    if todo.get("id") == id:
                        if body.get("todo") != None :
                            todo.update({"todo": body["todo"]})
                        if body.get("done") != None :
                            todo.update({"done": bool(body["done"])})

                return jsonify({ "success": True, "items": items })
            else:
                return jsonify({ "success": False })
        else:
            return jsonify({ "success": True, "message": "No todo with that id" })
        
    elif request.method == "DELETE":        
        
        idExist = False 

        for item in items:
            if item.get("id") == id:
                idExist = True
        
        if idExist == True:
            for index, item in enumerate(items):
                if item.get("id") == id:
                    del items[index]
        
            return jsonify({ "success": True })
        else:
            return jsonify({ "success": True, "message": "No todo with that id" })