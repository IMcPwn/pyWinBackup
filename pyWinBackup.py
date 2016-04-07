#!/usr/bin/env python
# pyWinBackup.py by IMcPwn
# Copyright (C) 2016 Carleton Stuberg

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For the latest code and contact information visit: http://imcpwn.com

import os
import time
from time import gmtime, strftime
import base64
import subprocess
import sys
import fnmatch

def exit_msg():
  print("[X] Quitting...")
  sys.exit(1)

def print_error(error):
  subprocess.call("cmd.exe /c echo \"" + str(error) + "\" && pause")

def copy_files():
  try:
    for i in files_to_copy:
      if type(i) is list:
        for x in i:
	      curr_file = x
	      if os.path.isfile(curr_file):
	        print("[*] Copying " + curr_file + " to " + destination)
	        subprocess.Popen("xcopy \"{0}\"  \"{1}\\{2}\\\" /E /C /Q /R /Y /Z /I".format(curr_file, destination, backup_name), shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo).wait()
	      else:
	        print("[X] Error. " + curr_file + " does not exist. Skipping it.")	
      else:
	    curr_file = i
	    if os.path.isfile(curr_file):
	      print("[*] Copying " + curr_file + " to " + destination)
	      subprocess.Popen("xcopy \"{0}\"  \"{1}\\{2}\\\" /E /C /Q /R /Y /Z /I".format(curr_file, destination, backup_name), shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo).wait()
	    else:
	      print("[X] Error. " + curr_file + " does not exist. Skipping it.")
  except Exception as e:
    #print_error(e)
	pass

def find_files():
  for i in files_to_find:
    curr_path = findpatt(i, drive_to_search)
    if len(curr_path) > 0:
	  files_to_copy.append(curr_path)

def copy_dirs():
  if os.path.isdir(homepath):
      print("[*] %s exists") % homepath
      try:
        for i in dirs_to_copy:
          if os.path.isdir(homepath + "\\" + i):
            print("[*] Copying " + homepath + "\\" + i + " to " + destination)
            copy = subprocess.Popen("xcopy \"{0}\\{1}\"  \"{2}\\{3}\\{4}\" /E /C /Q /R /Y /Z /I".format(homepath, i, destination, backup_name, i), shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo).wait()
          else:
            print("[X] Error. " + homepath + "\\" + i + " does not exist. Skipping it.")
      except Exception as e:
	    #print_error(e)
		pass
  else:  
      print("[X] %s does not exist.") % homepath
	  
def connect():
  try:
    connect = subprocess.Popen("net use " + destination + " /user:" + username + " " + base64.b64decode(p), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
    connect.wait()
  except Exception as e:
    #print_error(e)
	pass
  try:
    msg = connect.stdout.read()
    if "successfully" not in msg:
      print("[X] Could not connect to " + destination)
      exit_msg()
  except Exception as e:
    exit_msg()
  print("[*] Connected to " + destination + " successfully.")

def disconnect():
  try:
    subprocess.Popen("net use " + destination + " /delete /y", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo).wait()
  except Exception as e:
    #print_error(e)
	pass

def findpatt(pattern, path):
  try:
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
  except Exception as e:
    #print_error(e)
    pass
  
def makeTimeStamp(done):
  try:
    currDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    with open(destination + "\\" + backup_name + "\\backup-status.txt", 'a') as outfile:
      if done:
	    print("[*] Backup completed on: " + currDate)
	    outfile.write("\nBackup completed on: " + currDate)
      else:
	    print("[*] Backup started on: " + currDate)
	    outfile.write("\nBackup started on: " + currDate)
  except Exception as e:
    #print_error(e)
    pass


if __name__ == "__main__":
  try:
    if os.name != 'nt':
       print("This program only works on windows.")
       exit_msg()
	   
    homepath = os.path.expanduser('~')
    # There's probably a better way to find the user's username
    user = os.getenv('USERNAME')
  
    files_to_copy = []
	
    isBackupFinished = False

### STUFF TO CHANGE ###
    # Files to find (and copy) (star is ok)
    files_to_find = ["*.pst", "*.nk2"]
    # Drives to search for the files on (default inside home directory)
    drive_to_search = homepath
    # Directories inside home directory to copy
    dirs_to_copy = ["Desktop", "Documents", "Favorites", "My Documents"]
    backup_name = str(user + "-" + time.strftime("%d-%m-%Y"))
    # DO NOT END DESTINATION WTIH \\
    # One backslash in the path needs to be two backslashes.
    destination = "\\\\windows-share\\backup-folder"
    username="backup-user"
    # I compile my script with pyinstaller so most people can't recover the password.
    # THIS IS STILL ENTIRELY INSECURE. 
    # DO NOT PUT ANY SENSITIVE CREDENTIALS IF THIS SCRIPT IS GOING ON PRODUCTION COMPUTERS
    p="cGFzc3dvcmQ="
### END STUFF TO CHANGE ###

    # Hide window for things opened with subprocess
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
  
    print("---- Welcome to pyWinBackup by IMcPwn ----\n\nFor help/the latest version visit http://imcpwn.com\n\n" + ("-" * 51) + "\n")
  
    print("[*] Attempting to disconnect from " + destination + " in case already connected.\n")
    disconnect()
  
    print("[*] Connecting to " + destination)
    connect()
	
    if not os.path.exists(destination + "\\" + backup_name):
      os.mkdir(destination + "\\" + backup_name)
	
    isBackupFinished = False
    makeTimeStamp(isBackupFinished)
	
    find_files()
    copy_files()
    copy_dirs()
	
    isBackupFinished = True
    makeTimeStamp(isBackupFinished)
  
    print("[*] Disconnecting from " + destination)
    disconnect()
    print("[^] Done!")
  except Exception as e:
    #print_error(e)
	pass
