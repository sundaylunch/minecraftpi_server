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

def try_to_connect():
    global mc

    tries=0
    while mc == None:
        try:
            tries+=1
            mc = minecraft.Minecraft.create()
            print("Connected to "+mc)
            return True
        except:
            print("Failed to connect retry..")
            if tries<3:
                continue
            else:
                print("Failed to connect")
                return False
  

@app.route("/chat")
def chat():
    global mc
    if mc==None:
           if try_to_connect()==False:
               message={"msg":"Failed to connect to minecraft at localhost"}
               return jsonify(message)
           
    msg = request.args.get("msg", "Hello from scratcher!")
    mc.postToChat(msg)
    message={"success": True, "msg":"chat posted to minecraft at localhost"}
    return jsonify(message)

@app.route("/getBlock")
def getBlock():
    global mc
    if mc==None:
           if try_to_connect()==False:
               message={"msg":"Failed to connect to minecraft at localhost"}
               return jsonify(message)
    
    
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


    
