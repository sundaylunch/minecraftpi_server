from flask import Flask
from flask import request
from markupsafe import escape
from flask import make_response
from flask import jsonify

from flask_cors import CORS
from mcpi import minecraft


mc = None
app = Flask(__name__)
CORS(app)

@app.route("/chat")
def chat():
    global mc
    tries=0
    while mc == None:
        try:
            tries+=1
            mc = minecraft.Minecraft.create()
            print("Connected tp "+mc)
        except:
            print("Failed to connect")
            if tries<3:
                pass
            message={"msg":"Failed to connect to minecraft at localhost"}
            return jsonify(message)
    msg = request.args.get("msg", "Hello from scratcher!")
    mc.chat(msg)
    message={"success": True, "msg":"chat posted to minecraft at localhost"}
    return jsonify(message)

@app.route("/getBlock")
def getBlock():
    x=request.args.get("x")
    y=request.args.get("y")
    z=request.args.get("z")
    print(x,y,z)
    message={"id":1}
    return jsonify(message)


    
