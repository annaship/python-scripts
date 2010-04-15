import os
import sys
import subprocess

files_dir = "/Users/anna/work/web_app/perl_tf/webservices/ruby/spec/test_web/"
# files = os.listdir("/Library/Webserver/Documents/")
files = os.listdir(files_dir)
# taxon_finder_client_spec2.rb

for f in files:
    #st = "python "+"Nclient.py "+"18/"+f+" >"+"results--"+f
    # print f
    #p = subprocess.Popen("ruby "+"Nclient.py "+"18/"+f+" >"+"results--"+f,shell=True)
    # p = subprocess.Popen("ruby "+"filename.rb "+f, shell=True)
    p = subprocess.Popen("spec "+files_dir+f, shell=True)
    
    
