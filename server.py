import threading
import logging
from audio.audio import Audio
from video.video import Video
from datetime import datetime
import os
import keyboard
from video.OpenPoseClassPython import OPVideo
from pynput import keyboard as kb
import socket
from mongo import mongo

mg = mongo()

class actividad:
	def __init__(self, root):
		t = datetime.now()
		self.data = {
			"root": root,
			"audioFile": root + "/audio.wav",
			"video1File": root + "/video1.avi",
			"video2File": root + "/video2.avi",
			"video3File": root + "/video3.avi",
			"video4File": root + "/video4.avi",
			"videoout1File": root + "/videoout1.avi",
			"videoout2File": root + "/videoout2.avi",
			"videoout3File": root + "/videoout3.avi",
			"videoout4File": root + "/videoout4.avi",
			"creationTime": datetime.today(),
			"startRecording": "",
			"endRecording": ""
		}
		self.id = mg.insert_one("Activities",self.data)
	
	def startRecording(self):
		newvalues = { "$set": { "startRecording": datetime.today() } }
		mg.update_one("Activities", self.id, newvalues) 
	
	def endRecording(self):
		newvalues = { "$set": { "endRecording": datetime.today() } }
		mg.update_one("Activities", id = self.id, newvalues = newvalues )

class server:
	"""Servidor"""
	ta = ""
	tv1 = ""
	tv2 = ""
	tv3 = ""
	tv4 = ""

	def __init__(self):
		self.ip_server = "192.168.1.128"
		self.portAudio = 5000
		self.port1 = 5001
		self.port2 = 5002
		self.port3 = 5003
		self.port4 = 5004
		
	
	def configActividad(self):
		NombreActividad= datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
		root = 'db/'+ NombreActividad
		os.makedirs(root, exist_ok=True)
		self.act = actividad(root)
		print("configured activity")
	
	def activate(self):
		self.ta = Audio(ipServer=self.ip_server, portAudio = self.portAudio, file = self.act.data["audioFile"], mg = mg, idAct = self.act.id)
		self.tv1 = Video(ipServer=self.ip_server, port = self.port1, file = self.act.data["video1File"])
		self.tv2 = Video(ipServer=self.ip_server, port = self.port2, file = self.act.data["video2File"])
		self.tv3 = Video(ipServer=self.ip_server, port = self.port3, file = self.act.data["video3File"])
		self.tv4 = Video(ipServer=self.ip_server, port = self.port4, file = self.act.data["video4File"])
		print("activated")

	def start(self):
		self.ta.start()
		self.tv1.start()
		self.tv2.start()
		self.tv3.start()
		self.tv4.start()
		print("listening")
	
	def record(self):
		self.ta.record()
		self.tv1.record()
		self.tv2.record()
		self.tv3.record()
		self.tv4.record()
		self.act.startRecording()
		print("recording")

	def finished(self):
		self.ta.finished()
		self.tv1.finished()
		self.tv2.finished()
		self.tv3.finished()
		self.tv4.finished()
		self.act.endRecording()
		print("finished")
	
	def processVideo(self):
		self.op = OPVideo(mg = mg)
		self.op.getKeyPointsVideo(input = self.act.data["video1File"], outputV = self.act.data["videoout1File"],idact = self.act.id,iduser=0)
		logging.debug("video1")
		self.op = OPVideo(mg = mg)
		self.op.getKeyPointsVideo(input = self.act.data["video2File"], outputV = self.act.data["videoout2File"],idact = self.act.id,iduser=1)
		logging.debug("video2")
		self.op = OPVideo(mg = mg)
		self.op.getKeyPointsVideo(input = self.act.data["video3File"], outputV = self.act.data["videoout3File"],idact = self.act.id,iduser=2)
		logging.debug("video3")
		self.op = OPVideo(mg = mg)
		self.op.getKeyPointsVideo(input = self.act.data["video4File"], outputV = self.act.data["videoout4File"],idact = self.act.id,iduser=3)
		logging.debug("video4")
		del self.op


if __name__ == '__main__':

	s = server()

	def pulsa(tecla):
		print ("tecla " + str(tecla))
		if tecla == kb.KeyCode.from_char('a'):
			s.configActividad()
		if tecla == kb.KeyCode.from_char('s'):
			s.activate()
		if tecla == kb.KeyCode.from_char('l'):
			s.start()
		if tecla == kb.KeyCode.from_char('r'):
			s.record()
		if tecla == kb.KeyCode.from_char('f'):
			s.finished()
		if tecla == kb.KeyCode.from_char('p'):
			s.processVideo()
		if tecla == kb.KeyCode.from_char('q'):
			exit(0)
		else:
			return True

	print("--")
	kb.Listener(pulsa).run()

	# ooo = OPVideo()
	# ooo.getKeyPointsVideo(video1File,"out.avi","data.dat")