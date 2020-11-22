#-*- encoding: utf-8 -*-
# Now works in python 3 aswell as 2

import sys, threading, time, os, datetime, time, inspect, subprocess, socket
from subprocess import PIPE, STDOUT
import json
from audio.audio import Audio
from video.video import Video
from datetime import datetime
import signal
from mongo import mongo
from bson.objectid import ObjectId
mg = mongo()

ip_server = "192.168.1.128"
portAudio = 5000
port1 = 5001
port2 = 5002
port3 = 5003
port4 = 5004

# ------------------ terrible daemon code for windows -------------------
if __name__ == '__main__':

	Windows = sys.platform == 'win32'
	ProcessFileName = os.path.realpath(__file__)
	pidName = ProcessFileName.split('\\')[-1].replace('.py','')
	if Windows:
		pidFile = 'c:\\Windows\\Temp\\'+pidName+'.pid'
	else:
		pidFile = '/tmp'+pidName+'.pid'

	def start(pidfile, pidname, args):
		""" Create process file, and save process ID of detached process """
		pid = ""
		if Windows:
			#start child process in detached state
			DETACHED_PROCESS = 0x00000008
			p = subprocess.Popen([sys.executable, ProcessFileName, "child", args], creationflags=DETACHED_PROCESS)
			pid = p.pid

		else:
			p = subprocess.Popen([sys.executable, ProcessFileName, "child", args], stdout = PIPE, stderr = PIPE)
			pid = p.pid


		print("Service", pidname, pid, "started", flush=True)
		# create processfile to signify process has started
		with open(pidfile, 'w') as f:
			f.write(str(pid))
		f.close()
		os._exit(0)


	def stop(pidfile, pidname, args):
		""" Kill the process and delete the process file """
		procID = ""
		try:
			with open(pidfile, "r") as f:
				procID = f.readline()
			f.close()
		except IOError:
			print("process file does not exist, but that's ok <3 I still love you", file = sys.stderr, flush=True)

		if procID:
			if Windows:
				try:
					killprocess = subprocess.Popen(['taskkill.exe','/PID',procID,'/F'], stdout = PIPE, stderr = PIPE)
					killoutput = killprocess.communicate()

				except Exception as e:
					print(e)
					print ("could not kill ", procID, file = sys.stderr, flush=True)
				else:
					print("Service", pidname, procID, "stopped", flush=True)

			else:
				try:
					subprocess.Popen(['kill','-SIGTERM',procID])
				except Exception as e:
					print(e)
					print("could not kill " + procID, file = sys.stderr, flush=True)
				else:
					print("Service " + procID + " stopped", flush=True)

			#remove the pid file to signify the process has ended
			os.remove(pidfile)

	if len(sys.argv) <= 3: #2

		if sys.argv[1] == "start":
			args = sys.argv[2]
			if os.path.isfile(pidFile) == False:
				start(pidFile, pidName, args)
			else:
				print("process is already started", file = sys.stderr, flush=True)

		elif sys.argv[1] == "stop":
			args = sys.argv[2]
			if os.path.isfile(pidFile) == True:
				stop(pidFile, pidName, args)
			else:
				print("process is already stopped", file = sys.stderr, flush=True)

		elif sys.argv[1] == "restart":
			args = sys.argv[2]
			stop(pidFile, pidName,args)
			start(pidFile, pidName,args)
		
		elif sys.argv[1] == "end":
			os.remove(pidFile)
			print("delete pidfile", flush=True)

		# This is only run on windows in the detached child process
		elif sys.argv[1] == "child":
			print("child", flush=True)
			data = json.loads(sys.argv[2])
			print("data", flush=True)
			#id_ = mg.insert_one("test",{"test":data["id"],"test2":ObjectId(data["id"])})
			print("test", flush=True)
			ta = Audio(ipServer=ip_server, portAudio = portAudio, file = data["audioFile"], mg = mg, idAct = data["id"])
			tv1 = Video(ipServer=ip_server, port = port1, file = data["video1File"])
			tv2 = Video(ipServer=ip_server, port = port2, file = data["video2File"])
			tv3 = Video(ipServer=ip_server, port = port3, file = data["video3File"])
			tv4 = Video(ipServer=ip_server, port = port4, file = data["video4File"])
			print("video", flush=True)
			ta.start()
			tv1.start()
			tv2.start()
			tv3.start()
			tv4.start()
			print("start", flush=True)
			ta.record()
			tv1.record()
			tv2.record()
			tv3.record()
			tv4.record()
			print("record", flush=True)
			newvalues = { "$set": { "startRecording": datetime.today() } }
			mg.update_one("Activities", id = ObjectId(data["id"]), newvalues = newvalues )
			print("startRecording", flush=True)
			time.sleep(int(data["durationOfActivity"]) * 60)
			print("sleep", flush=True)
			ta.finished()
			tv1.finished()
			tv2.finished()
			tv3.finished()
			tv4.finished()
			print("finished", flush=True)
			newvalues = { "$set": { "endRecording": datetime.today() } }
			mg.update_one("Activities", id = ObjectId(data["id"]), newvalues = newvalues )
			print("endRecording", flush=True)
	else:
		print("usage: python "+pidName+".py start|stop|end|restart", flush=True)

#kill main
os._exit(0)