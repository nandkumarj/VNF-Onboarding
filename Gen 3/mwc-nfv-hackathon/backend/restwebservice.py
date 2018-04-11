##########################################################################
##
# Copyright 2017-2018 VMware Inc.
# This file is part of VNF-ONboarding
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# For those usages not covered by the Apache License, Version 2.0 please
# contact:  osslegalrouting@vmware.com

##

############################################################################

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict

from rest_generate_blueprint import rest_create_blueprint_package, rest_cleanup,rest_gen_name_and_workdir
from database import db_check_credentials,db_user_signup,db_generate_newpassword,db_update_user_with_token,db_delete_token_from_user,db_check_token
import logging
from logging.handlers import RotatingFileHandler
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from sendemail import sendMail,draft_mail_text
from flask_jwt import JWT, jwt_required, current_identity
from  catalog import _getVIMs,_getOrchsforVIM,_getInputHeads,_getInputHeadDetails

import resources
from prefixmiddleware import PrefixMiddleware
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from flask_jwt_extended import JWTManager
from functools import wraps
import json
import jwt
import datetime
import os
import pprint
app = Flask(__name__)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/api')

#jwt = JWT(app)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['REST_ROUTE_V1'] = '/api/v1'
app.config['APPLICATION_ROOT'] = '/backend/app'

@app.route('/',methods=['GET'])

def init():
  return jsonify({"Message" : "Welcome"})

@app.route('/v1/Login',methods=['POST'])

@cross_origin(origin='*')

def login():
  if request.method == 'POST':
     print "Received Login request:",request.data
  if request.data == "":
     return jsonify({"Error":"User Credentials not provided",'status': '200'})

  auth = json.loads(request.data)
  if not auth or not auth['username'] or not auth['password']:
      return jsonify({'Message':'Bad Request or UserName or Password Missing in request data','status': '200'})
  credentials = auth
  print(credentials['username'] ,credentials['password'])
  if db_check_credentials(credentials['username'] ,credentials['password']):
        print "Login Successfull for user",credentials['username']
        token = jwt.encode({'username':credentials['username'],'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 180)},app.config['JWT_SECRET_KEY'])
        #return jsonify({'token': token.decode('UTF-8')})
        print "login:",token
        db_update_user_with_token(credentials['username'],token)
        return jsonify({'token': token,'status':'200'})
  return jsonify({'Message' : "Authentication Failed",'status':'200'})




@app.route('/v1/RegisterUser',methods=['POST'])

def RegisterUser():
  if request.method == 'POST':
     print "Received User Registration Request"
     print "Register User:received signup request"
     if request.data:
        print "Request Data:",request.data
        #credentials = request.data
        credentials = json.loads(request.data)
        
        print(credentials['username'],credentials['password'])
     elif request.form:
        credentials = request.form
        print "Register User:",credentials


     status = db_user_signup(credentials['username'],credentials['password'],credentials['emailaddress'])
     print(status)
     if(status == "True"):
        mail_text = draft_mail_text("User Registration",credentials['username'],credentials['password'])
        print "signup:",mail_text
        sendMail([credentials['emailaddress']],"Rest Service VNF Onboarding User Registration",mail_text)
        return jsonify({"Success": "Registraton Succeeded for User {}".format(credentials['username']),"status" : "200"})  
     else:
        return jsonify({'Failure':"User or Email ID exists", "status": "200"}) 


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
	currentUser = None
        if 'x-access-token' in request.headers:
	   token = request.headers['x-access-token']
           print "token_required",token
        if not token:
           return jsonify({"Error": "token is missing",'status':'200'})
        try:
           data = jwt.decode(token,app.config['JWT_SECRET_KEY'],'UTF-8')
           print "token_rquired",data
           currentUser = data['username']
           print "Received token for User:",currentUser
        except:
	   return jsonify({"message" : "invalid token or token expired"})


        if db_check_token(currentUser) != token:   
           return jsonify({"Error" : "User is Logged out"})

        return f(currentUser,*args,**kwargs)
    return decorated           
 
@app.route('/protected',methods=['GET','POST'])
@token_required
def protected(currentUser):
  print "Received request on protected end point"
  return jsonify({"Message": "Invoked Protected API for {}".format(currentUser)})



@app.route('/v1/VIMS',methods=['GET'])
@token_required
def listvims(currentUser):
   if request.method == 'GET':
      return jsonify({"Success":"List of Supported VIMS","VIMS":_getVIMs()})

@app.route('/v1/Orchestrators' ,methods = ['GET'])
@token_required
def getOrchs(currentUser):
   if request.method == 'GET':   
      vim = request.args.get('vim')
      print "getOrchs: vim:",vim
      if vim in _getVIMs():
        return jsonify({"Success" : "List of Supported Orchestrators", "Orchestrators" : _getOrchsforVIM(vim),'status': '200'})
      else:
        return jsonify({"Failure": "Unsupported VIM {}".format(vim),'status':'200'})


@app.route('/v1/VNF Types' ,methods = ['GET'])
@token_required
def listVNFTypes(currentUser):
   if request.method == 'GET':
      vim = request.args.get('vim')
      orch = request.args.get('orch')
      print "getOrchs: vim:",vim
      if vim in _getVIMs() and orch in _getOrchsforVIM(vim):
         return jsonify({"Success" : "List of Supported VNFs", "VNF Types" : _getOrchsforVIM(vim),'status': '200'})
      else:
         return jsonify({"Failure": "Unsupported VIM {}".format(vim),'status':'200'})



@app.route('/v1/InputHeads',methods = ['GET'])
@token_required
def getInputHeads(currentUser):
    if request.method == 'GET':
       vim = request.args.get('vim')
       orch = request.args.get('orch')
       print "getInputHeads: vim:{},Orch:{}".format(vim,orch)
       if vim in _getVIMs() and orch in _getOrchsforVIM(vim):
          return jsonify({"Success" : "Retrieved Input Heads", "InputHeads":"InputHeads for vim :{} and Orch:{} are:{}".format(vim,orch,_getInputHeads(vim,orch))})
       else :
          return jsonify({"Failure" : "VIM or Orchestrator not supported",'status':'200'})

@app.route( '/v1/InputHeadDetails',methods = ['GET'])
@token_required
def getInputHeadDetails(currentUser):
    if request.method == 'GET':
       vim = request.args.get('vim')
       orch = request.args.get('orch')
       inputHead = request.args.get('inputHead')
       print "getInputHeadDetails: vim:{},Orch:{},inputHead:{}".format(vim,orch,inputHead)
       if vim in _getVIMs():
         print "vim present",vim

       if orch in _getOrchsforVIM(vim):
         print "Orch present",orch
      
       if inputHead in _getInputHeads(vim,orch):
          print "inputHead present",inputHead
       else:
          print "not present",inputHead,_getInputHeads(vim,orch)
       if vim in _getVIMs() and orch in _getOrchsforVIM(vim) and inputHead in _getInputHeads(vim,orch):
            return jsonify({"Success" : "Retrieved Details for InputHead:{} for {} + {} combination ".format(inputHead,vim,orch), "Data": _getInputHeadDetails(vim,orch,inputHead)})
       else:
            return jsonify({"Failure": "Could not find {} Details for {} + {}".format(inputHead,vim,orch)})



@app.route('/v1/generateBlueprint',methods = ['POST'])
@token_required
def generateblueprint(currentUser):
    if request.method == 'POST':
       inputs = request.get_json(request.data)
       #app.logger.warning("Input Received: %s\n",inputs)
       #app.logger.warning("username is : %s\n",inputs['params']['username'])

       print("Inputs Received: %s\n",inputs)
       output_file, workdir = create_blueprint_package(inputs)
       print("backend:workdir=%s\n",workdir)
       resp = send_from_directory(directory=os.path.dirname(workdir),
                               filename=os.path.basename(output_file),
                               as_attachment=True,
                               attachment_filename=os.path.basename(output_file))
       cleanup(os.path.dirname(workdir))
       return resp


@app.route('/v1/blueprint',methods=['POST'])
@token_required
def upload(currentUser):
   if request.method == 'POST':
      print("Received upload request")

   pprint.pprint(request.files) 
   #if not request.files:
   #  return jsonify({"Error" : "No Files to Upload"})
   formdata_dict = ImmutableMultiDict(request.form).to_dict()
   print "upload Formdata dict:",formdata_dict
   fddjs = json.dumps(formdata_dict)
   print "fddjs:",fddjs
   fddjson = json.loads(fddjs)
   print "fddjson:",fddjson
   #vim = request.form['VIM']
   #orch = request.form['Orch']
   vim = fddjson['env_type']
   orch = fddjson['Orch']
   print "vim,orch",vim,orch
   inputs = {}
   inputs['params'] = fddjson
   inputs['params']['username'] = currentUser
   inputs['params']['orch_type'] = inputs['params']['Orch']
   print "inputs",inputs
   uploaded_files = []
   if request.files:
      if orch  in _getOrchsforVIM(vim):
         inputs['params']['scripts'] = {}
         name, workdir = rest_gen_name_and_workdir(inputs)
         scripts_dir = os.path.join(workdir,'scripts')
         os.mkdir(scripts_dir)
         if orch == 'OSM 3.0' or orch == 'RIFT.ware 5.3':
              print "\\\\n *****************\\\\\\\n"
              if 'cloud_init_script' in request.files.keys():
                print "/n **** OSM or Riftware *****" 
                cloud_init_script = request.files['cloud_init_script']
                script_name = secure_filename(cloud_init_script.filename)
                cloud_init_script.save(os.path.join(scripts_dir,script_name))
                uploaded_files.append(script_name)
                inputs['params']['scripts']['create'] = script_name
              else:
	        return jsonify({"Error":"cloud_init_script not provided"})
         else:
           if 'create' in request.files.keys():
             create_script = request.files['create']
             script_name = secure_filename(create_script.filename)
             create_script.save(os.path.join(scripts_dir,script_name))
             uploaded_files.append(script_name)
             inputs['params']['scripts']['create'] =  script_name

           if 'config' in request.files.keys():
             config_script = request.files['config']
             config_script_name = secure_filename(config_script.filename)
             config_script.save(os.path.join(scripts_dir,config_script_name))
             uploaded_files.append(config_script_name)
             inputs['params']['scripts']['config'] = config_script_name

           if 'delete' in request.files.keys():
             delete_script = request.files['delete']
             delete_script_name = secure_filename(delete_script.filename)
             delete_script.save(os.path.join(scripts_dir,delete_script_name))
             uploaded_files.append(delete_script_name)
             inputs['params']['scripts']['delete'] = delete_script_name
       
           if not uploaded_files:
              return ({"Error" : "File upload Failed"})

   print "Received: ",inputs
   output_file, workdir = rest_create_blueprint_package(inputs)
   print("backend:workdir=%s\n",workdir)
   resp = send_from_directory(directory=os.path.dirname(workdir),
                   filename=os.path.basename(output_file),
                   as_attachment=True,
                   attachment_filename=os.path.basename(output_file))
   rest_cleanup(os.path.dirname(workdir))
   return resp



@app.route('/v1/Logout',methods=['POST'])
@token_required
def logout(currentUser):
    if db_delete_token_from_user(currentUser) == True:
       return jsonify({"Success" : "user {} is logged out".format(currentUser)})

  

if __name__ == '__main__':
     app.run('0.0.0.0',port=3005,debug=True)
