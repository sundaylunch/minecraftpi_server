from flask import Flask
from flask import request
from markupsafe import escape
from flask import make_response
from flask import jsonify

from flask_cors import CORS
from mcpi import minecraft

HOST="localhost"

mc = None
app = Flask(__name__)
CORS(app)

def try_to_connect():
    global mc

    tries=0
    while mc == None:
        try:
            tries+=1
            print("Tring to connect to minecraft at {}".format(HOST))
            mc = minecraft.Minecraft.create(HOST)
            print("Connected to "+HOST)
            message={"success": True, "msg":"Connected to {}".format(HOST)}
            return message
        except:
            print("Failed to connect retry..")
            if tries<3:
                continue
            else:
                print("Failed to connect")
                message={"success": False, "msg":"Failed to connect to {}".format(HOST)}
                return message

@app.route("/connect")
def connect():
     global mc, HOST
     HOST = request.args.get("host", "localhost")
     return jsonify(try_to_connect())
    
@app.route("/chat")
def chat():
    global mc
    if mc==None:
           resp=try_to_connect()
           if resp["success"]==False:
               return jsonify(resp)
           
    msg = request.args.get("msg", "Hello from scratcher!")
    mc.postToChat(msg)
    message={"success": True, "msg":"chat posted to minecraft at {}".format(HOST)}
    return jsonify(message)

@app.route("/getBlock")
def getBlock():
    global mc
    if mc==None:
           resp=try_to_connect()
           if resp["success"]==False:
               return jsonify(resp)
   
    x=request.args.get("x")
    y=request.args.get("y")
    z=request.args.get("z")
    
    try:
         x=float(x)
         y=float(y)
         z=float(z)

         id=mc.getBlock(x,y,z)
         print(f"Got block at {x}, {y}, {z} as {id}")
         message={"id":id}
    except:
         message={"msg":"invalid co-ordinates"}
    return jsonify(message)

@app.route("/setPos")
def setPos():
    global mc
    if mc==None:
           resp=try_to_connect()
           if resp["success"]==False:
               return jsonify(resp)
   
    x=request.args.get("x")
    y=request.args.get("y")
    z=request.args.get("z")
    
    try:
         x=float(x)
         y=float(y)
         z=float(z)

         mc.player.setPos(x,y,z)
         print(f"Move to {x}, {y}, {z}")
         message={"msg":f"Move to {x}, {y}, {z}"}
    except:
         message={"msg":"invalid co-ordinates"}
    return jsonify(message)


@app.route("/getPos")
def getPos():
    global mc
    if mc==None:
           resp=try_to_connect()
           if resp["success"]==False:
               return jsonify(resp)
    
    pos=mc.player.getPos()
    print(f"Got pos as {pos}")
    msgstr=f"Got pos as {pos.x} {pos.y} {pos.z}"
    message={"msg":msgstr,"x":pos.x,"y":pos.y,"z":pos.z}

    return jsonify(message)
