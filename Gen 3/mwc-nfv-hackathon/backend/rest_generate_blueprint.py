#!/usr/bin/env/python

#########################################################################
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
 
###########################################################################

import argparse
from jinja2 import Template
import os
import requests
import shutil
import validators
import tempfile
import yaml
import subprocess
import tarfile
import hashlib
import time
from datetime import datetime

TEMPLATES_DIR = './templates'
TEMPLATES = {'OpenStack': 'OS-template.yaml',
             'TOSCA_OpenStack': 'OS-TOSCA-template.yaml',
             'CUSTOM_FLAVOR': 'CUSTOM-FLAVOR-template.yaml',
             'OSM_OpenStack': 'OS-OSM-template.yaml',
             'OSM_NSD_OpenStack': 'OS-OSM-NSD-template.yaml',
             'vCloud Director': 'VCD-template.yaml',
             'TOSCA_vCloud Director': 'VCD-TOSCA-template.yaml',
             'OSM_vCloud Director': 'VCD-OSM-template.yaml',
             'OSM_NSD_vCloud Director': 'VCD-OSM-NSD-template.yaml',
	     'RIFTware_OpenStack': 'OS-RIFTware-template.yaml',
             'RIFTware_NSD_OpenStack': 'OS-RIFTware-NSD-template.yaml',
             'VIO': 'VIO-template.yaml',
             'TOSCA_VIO': 'VIO-TOSCA-template.yaml',
             'OSM_VIO': 'VIO-OSM-template.yaml'}

session_dir = ''

def parse_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputs', required=True, metavar='<inputs_file_path>')
    return parser.parse_args()


def rest_gen_name_and_workdir(inputs):
    params = inputs['params']
    #name = params['vnf_type'] + '-' + params['orch_type'] + '-'+ params['env_type']
    name = params['vnf_type'] + '-' + params['env_type'] + '-' + params['vnfd_name']
    name = name.replace(" ", "")    #Replacing Spaces in Dir names, as it causes problem parsing
    upload_dir = "/tmp/uploads/rest"
    if not os.path.isdir(upload_dir):
       os.mkdir(upload_dir)
    user_dir =  os.path.join(upload_dir,params['username'])
    if not os.path.isdir(user_dir):
       os.mkdir(user_dir)
     
    workdir = os.path.join(user_dir, name)
    workdir = workdir.replace(" ", "")  #Replacing Spaces in Dir names, as it causes problem parsing
    if not os.path.exists(workdir):
    #	   return jsonify({"Error":"work directory exists"})
       os.mkdir(workdir)
    return name, workdir


def get_template(template_file):
    with open(template_file) as f:
        text = f.read()
    return Template(text)


def copy_README(inputs, workdir):
    README = 'README.md'
    template_file = os.path.join(TEMPLATES_DIR, README)
    with open(template_file) as f:
        text = f.read()
    rendered = Template(text).render(inputs['params'])
    out_file = os.path.join(workdir, README)
    with open(out_file, 'w') as f:
        f.write(rendered)


def get_file_from_url(url):
    return requests.get(url).text, ('.' + url).split('.')[-1]


def write_scripts_file(working_dir, script_phase, ext, body):
    if ext:
        ext = '.' + ext
    path = os.path.join(working_dir, script_phase + ext)
    with open(path, 'w') as f:
        f.write(body)
    return path


def create_work_dir(workdir):
    if not os.path.isdir(workdir):
       os.mkdir(workdir)


def rest_cleanup(workdir):
   print("gb:inside cleanup\n")
   if os.path.isdir(session_dir):
      print("gb:clenup:session_dir:%s\n",session_dir)
      shutil.rmtree(session_dir)
   else:
      print("gb:cleanup:workdir:%s\n",workdir)
      shutil.rmtree(workdir)

def create_package(name, workdir):
    shutil.make_archive(
        os.path.abspath(workdir),
        'zip',
        os.path.dirname(workdir),
        name)
    return workdir + '.zip'

def check_key(key,data):
   if key in data.keys():
     return True
   return False

def GetHashofDirs(directory, verbose=0):
  import hashlib, os
  SHAhash = hashlib.md5()
  if not os.path.exists (directory):
    return -1

  try:
    for root, dirs, files in os.walk(directory):
      for names in files:
        if verbose == 1:
          print 'Hashing', names
        filepath = os.path.join(root,names)
        try:
          f1 = open(filepath, 'rb')
        except:
          # You can't open the file for some reason
          f1.close()
          continue

        while 1:
          # Read file in as little chunks
          buf = f1.read(4096)
          if not buf : break
          SHAhash.update(hashlib.md5(buf).hexdigest())
        f1.close()

  except:
    import traceback
    # Print the stack traceback
    traceback.print_exc()
    return -2

  return SHAhash.hexdigest()

def copy_scripts(workdir,vnfd_dir):
    scripts_dir = os.path.join(workdir,'scripts')  
    vnfd_scripts_dir = os.path.join(vnfd_dir,'scripts')
    if not os.path.exists(vnfd_scripts_dir):
       print "copy_scripts: making vnfd scripts dir:",vnfd_scripts_dir
       os.mkdir(vnfd_scripts_dir)
    if os.path.exists(scripts_dir) and os.path.exists(vnfd_scripts_dir):
       src_files = os.listdir(scripts_dir)
       print("gb:list uploaded files:",src_files)
       for file_name in src_files:
           full_file_name = os.path.join(scripts_dir, file_name)
           print("gb:full file name:",full_file_name)
           if (os.path.isfile(full_file_name)):
               print("print file name %s\n", os.path.basename(full_file_name))
               shutil.copy(full_file_name, vnfd_scripts_dir)
       shutil.rmtree(scripts_dir)

  
def create_osm_vnfd_package(inputs, name, workdir):
    vnfd_dir = os.path.join(workdir, name + '_vnfd')
    os.mkdir(vnfd_dir)
    charms_dir = os.path.join(vnfd_dir, 'charms')
    os.mkdir(charms_dir)
    cloud_init_dir = os.path.join(vnfd_dir, 'cloud_init')
    os.mkdir(cloud_init_dir)
    icons_dir = os.path.join(vnfd_dir, 'icons')
    os.mkdir(icons_dir)
    images_dir = os.path.join(vnfd_dir, 'images')
    os.mkdir(images_dir)
    #add_scripts(inputs['params'], vnfd_dir)
    copy_scripts(workdir,vnfd_dir)
    generate_standard_osm_blueprint(inputs['params'], vnfd_dir, name)
    checksum = GetHashofDirs(vnfd_dir)
    checksums_file = os.path.join(vnfd_dir, 'checksums.txt')
    with open(checksums_file, 'w') as f:
        f.write(checksum)
    i = datetime.now()
    readme="Descriptor created by OSM descriptor package generated. \nCreated on " + i.strftime('%Y/%m/%d %H:%M:%S')
    readme_file = os.path.join(vnfd_dir, 'README.txt')
    with open(readme_file, 'w') as f:
        f.write(readme)
    vnfd_tar=shutil.make_archive(
        os.path.abspath(vnfd_dir),
        'gztar',
        os.path.dirname(vnfd_dir),
        name + '_vnfd')

    shutil.rmtree(vnfd_dir)
    return vnfd_tar

def create_osm_nsd_package(inputs, name, workdir):
    nsd_dir = os.path.join(workdir, name + '_nsd')
    os.mkdir(nsd_dir)
    ns_config_dir = os.path.join(nsd_dir, 'ns_config')
    os.mkdir(ns_config_dir)
    vnf_config_dir = os.path.join(nsd_dir, 'vnf_config')
    os.mkdir(vnf_config_dir)
    icons_dir = os.path.join(nsd_dir, 'icons')
    os.mkdir(icons_dir)
    #add_scripts(inputs['params'], nsd_dir)
    generate_standard_osm_nsd_blueprint(inputs['params'], nsd_dir, name)
    checksum = GetHashofDirs(nsd_dir)
    checksums_file = os.path.join(nsd_dir, 'checksums.txt')
    with open(checksums_file, 'w') as f:
        f.write(checksum)
    i = datetime.now()
    readme="Descriptor created by OSM descriptor package generated. \nCreated on " + i.strftime('%Y/%m/%d %H:%M:%S')
    readme_file = os.path.join(nsd_dir, 'README.txt')
    with open(readme_file, 'w') as f:
        f.write(readme)
    nsd_tar=shutil.make_archive(
        os.path.abspath(nsd_dir),
        'gztar',
        os.path.dirname(nsd_dir),
        name + '_nsd')
    shutil.rmtree(nsd_dir)
    return nsd_tar


def get_hash(fname, algo):
    import hashlib, os
    if algo == "SHA256":
        SHAhash = hashlib.sha256()
    elif algo == "MD5":
        SHAhash = hashlib.md5()
    else:
        print("Unknown SHA Algo. Exiting")
        return -2

    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(2 ** 20), b""):
            SHAhash.update(chunk)

    print("{} Hash of file {}: {}".format(algo, fname, SHAhash.hexdigest()))
    return SHAhash.hexdigest()

def copy_scripts_for_riftware(params, name,workdir,target,remove_scritps_dir=False):
    print("scripts dict :",params['scripts'])
    
    scripts_dir = os.path.join(workdir,'scripts')
    print "copy_scripts_for_riftware: scripts_dir",scripts_dir
    #upload_dir = os.path.join('/tmp/uploads',params['username'])
    #upload_scripts_dir = os.path.join(upload_dir,params['session_key'])

    scripts_dir = os.path.join(workdir, 'scripts')
    #os.mkdir(scripts_dir)
    vnfd_dir = ""
    nsd_scripts_dir = ""
    cloud_init_dir = ""

    if target == 'vnfd':
        print "target is vnfd"
        vnfd_dir = os.path.join(workdir, name + '_vnfd')
        cloud_init_dir = os.path.join(vnfd_dir, 'cloud_init')
        print "create cloud_init directory",cloud_init_dir 
        os.mkdir(cloud_init_dir)
    elif target == "nsd":
        nsd_dir = os.path.join(workdir,name + '_nsd')
        nsd_scripts_dir = os.path.join(nsd_dir,'scripts')
        os.mkdir(nsd_scripts_dir)

    print("RIFT.io Scripts uploaded to temp folder: ",cloud_init_dir)
    if os.path.isdir(scripts_dir):
        src_files = os.listdir(scripts_dir)
        print("RIFT.io - list of uploaded files in temp folder:",src_files)
        for file_name in src_files:
            full_file_name = os.path.join(scripts_dir, file_name)
            print("Before copying RIFT.io script - check if this is a valid file:",full_file_name)
            if (os.path.isfile(full_file_name)):
                if (file_name in params['scripts']['create']):
                    if target == 'vnfd':
                        print "Copying file {} to cloud_init_dir {}".format(full_file_name,cloud_init_dir)
                        shutil.copy(full_file_name, cloud_init_dir)
                        print("Copied file {} to cloud_init dir\n".format(os.path.basename(full_file_name)))
                else:
                    shutil.cipy(full_file_name, scripts_dir)
                    print("Copied file {} to scripts dir\n".format(os.path.basename(full_file_name)))
        if (remove_scritps_dir == True):
            shutil.rmtree(scripts_dir)

def create_riftware_manifest_file(name, directory):
  print("RIFT.io - Creating RIFT.ware manifest file for", name)
  VENDOR = "RIFT.io"
  VERSION = "1.0"
  DATE_TIME = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
  SHA_ALGO = "SHA256"

  mf_name = name + ".mf"
  mf_file = os.path.join(directory, mf_name)
  with open(mf_file, 'a') as f:
    f.write("Product-Name: {}\n".format(name))
    f.write("Provider-ID: {}\n".format(VENDOR))
    f.write("Package-Version: {}\n".format(VERSION))
    f.write("Release-Date-Time: {}\n".format(DATE_TIME))
    f.write("Package-State: new\n\n")
    try:
      for root, dirs, files in os.walk(directory):
        for fileName in files:
          if fileName.endswith(".mf"):
            continue
          relDir = os.path.relpath(root, directory)
          relFile = os.path.join(relDir, fileName)
          print 'Hashing ', relFile
          filepath = os.path.join(root,fileName)
          if relDir == "images":
                    # Keep image checksum to be MD5 for now
                    # as glance/openstack supports only that
            file_hash = get_hash(filepath, "MD5")
          else:
            file_hash = get_hash(filepath, "SHA256")
          f.write("Source: {}\n".format(relFile))
          f.write("Algorithm: {}\n".format(SHA_ALGO))
          f.write("Hash: {}\n\n".format(file_hash))
    except:
      import traceback
      # Print the stack traceback
      traceback.print_exc()
      return -2

def create_riftware_vnfd_package(inputs, name, workdir):
    print("RIFT.io - Creating RIFT.ware VNFD Package")
    vnfd_dir = os.path.join(workdir, name + '_vnfd')
    os.mkdir(vnfd_dir)
    charms_dir = os.path.join(vnfd_dir, 'charms')
    os.mkdir(charms_dir)
    icons_dir = os.path.join(vnfd_dir, 'icons')
    os.mkdir(icons_dir)
    images_dir = os.path.join(vnfd_dir, 'images')
    os.mkdir(images_dir)
    copy_scripts_for_riftware(inputs['params'],name,workdir,'vnfd')

    generate_standard_riftio_blueprint(inputs['params'], vnfd_dir, name)

    create_riftware_manifest_file(name+'_vnfd', vnfd_dir)
    copy_README(inputs, workdir)

    vnfd_tar=shutil.make_archive(
        os.path.abspath(vnfd_dir),
        'gztar',
        os.path.dirname(vnfd_dir),
        name + '_vnfd')

    shutil.rmtree(vnfd_dir)
    print("RIFT.io - Done creating RIFT.ware VNFD Package")
    return vnfd_tar

def create_riftware_nsd_package(inputs, name, workdir):
    print("RIFT.io - Creating RIFT.ware NSD Package")
    nsd_dir = os.path.join(workdir, name + '_nsd')
    os.mkdir(nsd_dir)
    ns_config_dir = os.path.join(nsd_dir, 'ns_config')
    os.mkdir(ns_config_dir)
    vnf_config_dir = os.path.join(nsd_dir, 'vnf_config')
    os.mkdir(vnf_config_dir)
    icons_dir = os.path.join(nsd_dir, 'icons')
    os.mkdir(icons_dir)
    copy_scripts_for_riftware(inputs['params'],name, workdir,'nsd',True)

    generate_standard_riftio_nsd_blueprint(inputs['params'], nsd_dir, name)

    create_riftware_manifest_file(name+'_nsd', nsd_dir)
    copy_README(inputs, workdir)

    nsd_tar=shutil.make_archive(
        os.path.abspath(nsd_dir),
        'gztar',
        os.path.dirname(nsd_dir),
        name + '_nsd')

    shutil.rmtree(nsd_dir)
    print("RIFT.io - Done creating RIFT.ware NSD Package")
    return nsd_tar



def get_orch_types(params):
        print "inside get_orch_types:",params['orch_type']
	orch = params['orch_type']
	## TODO : (this is workaround) need to will handle Cloudify 4.0 in proper way.
    
	#if params['orch_type'] == 'Cloudify 4.0':
	#   orch = 'Cloudify 3.4'
	   
	return orch 

def get_git_flag(params):
     uploadflag = params['git_upload']
     return uploadflag 

def get_env_types(params):
     env = params['env_type']
     return env 

def get_vnf_types(params):
     vnf = params['vnf_type']
     return vnf 

def get_flavor_type(params):
     flavor = params['flavor']
     return flavor 

   
def generate_cloudify_blueprint(params, workdir, name):
    template = get_template(os.path.join(TEMPLATES_DIR, TEMPLATES[params['env_type']]))
    print("Inside generate cloudify blueprint :%s\n",params)
    print("Print Template : %s\n",template)
    out = template.render(params)
    out_file = os.path.join(workdir, name + '.yaml')
    with open(out_file, 'w') as f:
        f.write(out)

def generate_standard_osm_blueprint(params, workdir, name):
    template = get_template(os.path.join(TEMPLATES_DIR, TEMPLATES['OSM_' + params['env_type']]))
    out = template.render(params)
    out_file = os.path.join(workdir, name + '_vnfd.yaml')
    with open(out_file, 'w') as f:
        f.write(out)

def generate_standard_osm_nsd_blueprint(params, workdir, name):
    template = get_template(os.path.join(TEMPLATES_DIR, TEMPLATES['OSM_NSD_' + params['env_type']]))
    out = template.render(params)
    out_file = os.path.join(workdir, name + '_nsd.yaml')
    with open(out_file, 'w') as f:
        f.write(out)

def generate_standard_riftio_blueprint(params, workdir, name):
    template = get_template(os.path.join(TEMPLATES_DIR, TEMPLATES['RIFTware_' + params['env_type']]))
    out = template.render(params)
    out_file = os.path.join(workdir, name + '_vnfd.yaml')
    with open(out_file, 'w') as f:
        f.write(out)

def generate_standard_riftio_nsd_blueprint(params, workdir, name):
    template = get_template(os.path.join(TEMPLATES_DIR, TEMPLATES['RIFTware_NSD_' + params['env_type']]))
    out = template.render(params)
    out_file = os.path.join(workdir, name + '_nsd.yaml')
    with open(out_file, 'w') as f:
        f.write(out)


def generate_riftio_package(params, workdir, name, create_nsd=True):
    vcpu = params['cpu']
    memory = params['ram']
    storage = params['disk']
    image = params['image_id']
    num_interfaces = -1 
    cinit_scripts_dir = os.path.join(workdir,'scripts')
    cinit_files = os.listdir(cinit_scripts_dir)
    if not cinit_files:
        cloud_init_file = None
    else:
        cloud_init_file = cinit_files[0]
        cloud_init = os.path.join(cinit_scripts_dir, cloud_init_file)
        print "In RIFT.io: cloud_init_file: %s" % (cloud_init)
    
    for key in params:
        if key.startswith("nic"):
            num_interfaces += 1 

    rift_cmd = "./generate_riftio_descriptor_pkg_5.3.sh -c -a {nsd} --vcpu {vcpu} --memory {memory} --storage {storage} --image {image} {cloud_init} --interfaces {interfaces} \"{out_file}\" \"{vnf_name}\"".format( vcpu=vcpu, 
                                    memory=memory, 
                                    storage= 0 if not storage else storage, 
                                    image=image, 
                                    cloud_init = "--cloud-init-file "+cloud_init if cloud_init_file is not None else "",
                                    interfaces=num_interfaces, 
                                    out_file=workdir, 
                                    vnf_name=name,
                                    nsd = "--nsd" if create_nsd else "")
    print "RIFT Generate Descriptor command: ", rift_cmd
    rc = subprocess.call(rift_cmd, shell=True)
    if rc != 0:
        print("ERROR: RIFT.ware Descriptor generation Failed!! Error: ", rc)
        raise

    ''' Remove the 'scripts' dir from the package, as RIFT.ware doesn't need it. 
        The files have already been copied to the correct folder inside the tar.gz package
    '''
    shutil.rmtree(cinit_scripts_dir)
    

def generate_standard_tosca_blueprint(params, workdir, name):
    print "Inside generate_standard_tosca_blueprint"
    template = get_template(os.path.join(TEMPLATES_DIR, TEMPLATES['TOSCA_' + params['env_type']]))
    out = template.render(params)
    out_file = os.path.join(workdir, name + '-TOSCA.yaml')
    with open(out_file, 'w') as f:
        f.write(out)
    shutil.copytree(os.path.join(TEMPLATES_DIR, 'types'), os.path.join(workdir, 'types'))
	


def generate_flavor_blueprint(params, workdir, name):
    template = get_template(os.path.join(TEMPLATES_DIR, TEMPLATES['CUSTOM_FLAVOR']))
    out = template.render(params)
    out_file = os.path.join(workdir, 'CUSTOM-FLAVOR.yaml')
    with open(out_file, 'w') as f:
        f.write(out)

def copy_inputs_template(params, workdir):
    inputs_name = params['env_type'] + '-inputs.yaml'
    name = inputs_name.replace(" ", "")    #Replacing Spaces in Dir names, as it causes problem parsing
    shutil.copyfile(os.path.join(TEMPLATES_DIR, inputs_name), os.path.join(workdir, name))


def remove_file(filepath):
    os.remove(filepath)


def rest_create_blueprint_package(inputs):
    name, workdir = rest_gen_name_and_workdir(inputs)
    try:
        create_work_dir(workdir)
        if get_orch_types(inputs['params']) != 'OSM 3.0':
           #add_scripts(inputs['params'], workdir)
           copy_README(inputs, workdir)
        print "The input parameter is ", get_orch_types(inputs['params']) 
        #print "The git flag is ", get_git_flag(inputs['params']) 
        print "The input list parameter is ", inputs['params'] 
        #commit_comment=get_env_types(inputs['params']) + '_' + get_orch_types(inputs['params']) + '_'+ get_vnf_types(inputs['params'])
        orch_name= get_orch_types(inputs['params'])
        env_name= get_env_types(inputs['params'])
        vnf_name= get_vnf_types(inputs['params'])
        if get_orch_types(inputs['params']) == 'Cloudify 3.4' or get_orch_types(inputs['params']) == 'Cloudify 4.0' : 
            generate_cloudify_blueprint(inputs['params'], workdir, name)
            if check_key('flavor',inputs['params']) and get_flavor_type(inputs['params']) == 'auto' and env_name == 'OpenStack':
                 generate_flavor_blueprint(inputs['params'], workdir, name)
            copy_inputs_template(inputs['params'], workdir)
            output_file = create_package(name, workdir)
            #print "The git flag outside ", get_git_flag(inputs['params']) 
            #if get_git_flag(inputs['params']) == True: 
             #   print "The git flag inside ", get_git_flag(inputs['params']) 
             #   print("params for git upload : output file = %s\n, workdir = %s\n,orch_name = %s\n,commit_comment = %s\n",output_file, workdir, orch_name, commit_comment)
#            #    Process=subprocess.call(['./git_upload.sh', output_file, workdir, orch_name, commit_comment])
             #   Process=subprocess.call(['./git_upload.sh', output_file, workdir, commit_comment, orch_name, env_name, vnf_name])
#            #    Process=subprocess.call(['./git_upload.sh', output_file, workdir])  
#            # Process=subprocess.call(['./git_upload.sh', output_file, workdir])
            return output_file, workdir
        elif get_orch_types(inputs['params']) == 'OSM 3.0':
           vnfd_package=create_osm_vnfd_package(inputs, name, workdir)
           nsd_package=create_osm_nsd_package(inputs, name, workdir)
           output_file = create_package(name, workdir)
           print "The git flag outside ", get_git_flag(inputs['params']) 
           if get_git_flag(inputs['params']) == True: 
               print "The git flag inside ", get_git_flag(inputs['params']) 
#               Process=subprocess.call(['./git_upload.sh', output_file, workdir])
               Process=subprocess.call(['./git_upload.sh', output_file, workdir, commit_comment, orch_name, env_name, vnf_name])
#           Process=subprocess.call(['./git_upload.sh', output_file, workdir])
           return output_file, workdir
        elif get_orch_types(inputs['params']) == 'RIFT.ware 5.3':
	   #generate_riftio_package(inputs['params'], workdir, name, True)
	   vnfd_package = create_riftware_vnfd_package(inputs, name, workdir)
	   nsd_package = create_riftware_nsd_package(inputs, name, workdir)
	   output_file = create_package(name, workdir)
	   return output_file, workdir
        elif get_orch_types(inputs['params']) == 'TOSCA 1.1':
           print "Generating Blueprint from TOSCA"
           generate_standard_tosca_blueprint(inputs['params'], workdir, name)
           if get_env_types(inputs['params']) == 'OpenStack':
               print "Dealing with Flavors in TOSCA"
               if check_key('flavor',inputs['params']) and  get_flavor_type(inputs['params']) == 'Custom Flavor':
                   generate_flavor_blueprint(inputs['params'], workdir, name)
           copy_inputs_template(inputs['params'], workdir)
           output_file = create_package(name, workdir)
           print "Got the output file", output_file
           print "Got the working directory",workdir 
#             Process=subprocess.Popen('./git_upload.sh %s' % (output_file), shell=True) 
           print "The git flag outside ", get_git_flag(inputs['params']) 
           if get_git_flag(inputs['params']) == True: 
                print "The git flag inside ", get_git_flag(inputs['params']) 
                Process=subprocess.call(['./git_upload.sh', output_file, workdir, commit_comment, orch_name, env_name])
#           Process=subprocess.call(['./git_upload.sh', output_file, workdir])
           return output_file, workdir
    finally:
        print("inside finally")
        rest_cleanup(workdir)


if __name__ == '__main__':
    args = parse_argv()
    with open(args.inputs) as f:
        inputs = yaml.load(f.read())
        output_file, workdir = create_blueprint_package(inputs)
#        print "Got the output file", output_file
#        Process=subprocess.Popen('./git_upload.sh %s' % (str(output_file)))
       # subprocess.call(["git_upload.sh","output_file"],shell=True)
        rest_cleanup(workdir)
