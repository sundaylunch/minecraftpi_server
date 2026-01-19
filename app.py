from flask import Flask
from flask import request
from markupsafe import escape
from flask import make_response
from flask import jsonify

from flask_cors import CORS
from mcpi import minecraft
import sys

HOST="localhost"
DEBUG=False

if sys.argv[1]=="on":
     DEBUG=True

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
     if DEBUG:
          message={"success": True, "msg":"Connected to {}".format(HOST)}
          return jsonify(message)
     return jsonify(try_to_connect())
    
@app.route("/chat")
def chat():
    global mc
    if not DEBUG:
        if mc==None:
               resp=try_to_connect()
               if resp["success"]==False:
                   return jsonify(resp)
           
    msg = request.args.get("msg", "Hello from scratcher!")
    if not DEBUG:
        try:
            mc.postToChat(msg)
            message={"success": True, "msg":"chat posted to minecraft at {}".format(HOST)}
        except:
             mc=None
             message={"success": False, "msg": "failed to connect to".format(HOST)}

    return jsonify(message)

@app.route("/getBlock")
def getBlock():
    global mc

    if mc==None and not DEBUG:
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

         if not DEBUG:
             id=mc.getBlock(x,y,z)
             print(id,type(id))
             if id==35:
                  blockdata=mc.getBlockWithData(x,y,z)
                  print(blockdata)
                  id=3500+blockdata.data
         else:
             id=101
            
         print(f"Got block at {x}, {y}, {z} as {id}")
         message={"id":id}
    except:
         message={"msg":"invalid co-ordinates"}
    return jsonify(message)

@app.route("/setBlock")
def setBlock():
    global mc
    if mc==None and not DEBUG:
           resp=try_to_connect()
           if resp["success"]==False:
               return jsonify(resp)
   
    x=request.args.get("x")
    y=request.args.get("y")
    z=request.args.get("z")
    block=request.args.get("block")
    data=request.args.get("data")
    
    try:
         x=float(x)
         y=float(y)
         z=float(z)
         block=int(block)
         data=int(data)
         
         if not DEBUG:
             mc.setBlock(x,y,z,block,data)
         print(f"set block at {x}, {y}, {z} as {block} with {data}")
         message={"msg":f"set block at {x}, {y}, {z} as {block} with {data}"}
    except Exception as e:
         print(e)
         message={"msg":"invalid request"}
    return jsonify(message)

@app.route("/setBlocks")
def setBlocks():
    global mc
    if mc==None and not DEBUG:
           resp=try_to_connect()
           if resp["success"]==False:
               return jsonify(resp)
   
    x=request.args.get("x")
    y=request.args.get("y")
    z=request.args.get("z")
    block=request.args.get("block")
    data=request.args.get("data")
    x1=request.args.get("x1")
    y1=request.args.get("y1")
    z1=request.args.get("z1")
    
    
    try:
         x=float(x)
         y=float(y)
         z=float(z)
         block=int(block)
         data=int(data)
         x1=float(x1)
         y1=float(y1)
         z1=float(z1)
         
         if not DEBUG:
             mc.setBlocks(x,y,z,x1,y1,z1,block,data)
         print(f"set block from {x}, {y}, {z} to {x1} {y1} {z1} as {block} with {data}")
         message={"msg":f"set block from {x}, {y}, {z} to {x1} {y1} {z1} as {block} with {data}"}
    except Exception as e:
         print(e)
         message={"msg":"invalid message"}
    return jsonify(message)


@app.route("/setPos")
def setPos():
    global mc
    if mc==None and not DEBUG:
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
         
         if not DEBUG:
             mc.player.setPos(x,y,z)
         print(f"Move to {x}, {y}, {z}")
         message={"msg":f"Move to {x}, {y}, {z}"}
    except:
         message={"msg":"invalid co-ordinates"}
    return jsonify(message)


@app.route("/getPos")
def getPos():
    global mc
    if mc==None and not DEBUG:
           resp=try_to_connect()
           if resp["success"]==False:
               return jsonify(resp)
    
    if not DEBUG:
        pos=mc.player.getPos()
    else:
        pos.x=123
        pos.y=111
        pos.z=321
        
    print(f"Got pos as {pos}")
    msgstr=f"Got pos as {pos.x} {pos.y} {pos.z}"
    message={"msg":msgstr,"x":pos.x,"y":pos.y,"z":pos.z}

    return jsonify(message)
