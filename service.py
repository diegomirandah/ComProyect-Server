import logging
from audio.audio import Audio
from video.video import Video
#from activity import activity
from datetime import datetime
from video.OpenPoseClassPython import OPVideo
import os

class activity:
	def __init__(self, root, mg, name, time_):
		self.mg = mg
		t = datetime.now()
		self.data = {
			"name": name,
			"durationOfActivity": time_,
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
		self.id = self.mg.insert_one("Activities",self.data)
		self.data["id"] = str(self.id)
		self.data.pop('_id')
		print(self.data)
	
	def get_data(self):
		return self.data

class service:
	"""Service"""
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
	
	def configActividad(self, name, time_, mg):
		NombreActividad = name
		root = 'db/'+ datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
		os.makedirs(root, exist_ok=True)
		act = activity(root, mg, NombreActividad, time_)
		logging.debug("configured activity")
		return act.get_data()
	
	def activate(self, audioFile, video1File, video2File, video3File, video4File, id_act, mg):
		self.ta = Audio(ipServer=self.ip_server, portAudio = self.portAudio, file = audioFile, mg = mg, idAct = id_act)
		self.tv1 = Video(ipServer=self.ip_server, port = self.port1, file = video1File)
		self.tv2 = Video(ipServer=self.ip_server, port = self.port2, file = video1File)
		self.tv3 = Video(ipServer=self.ip_server, port = self.port3, file = video1File)
		self.tv4 = Video(ipServer=self.ip_server, port = self.port4, file = video1File)
		logging.debug("activated")
	
	def start(self):
		self.ta.start()
		self.tv1.start()
		self.tv2.start()
		self.tv3.start()
		self.tv4.start()
		logging.debug("listening")
	
	def record(self):
		self.ta.record()
		self.tv1.record()
		self.tv2.record()
		self.tv3.record()
		self.tv4.record()
		self.act.startRecording()
		logging.debug("recording")

	def finished(self):
		self.ta.finished()
		self.tv1.finished()
		self.tv2.finished()
		self.tv3.finished()
		self.tv4.finished()
		self.act.endRecording()
		logging.debug("finished")
	
	def processVideo(self):
		self.op = OPVideo(mg = self.mg)
		self.op.getKeyPointsVideo(input = self.act.data["video1File"], outputV = self.act.data["videoout1File"],idAct = self.act.id,iduser=0)
		logging.debug("video1")
		self.op.getKeyPointsVideo(input = self.act.data["video2File"], outputV = self.act.data["videoout2File"],idAct = self.act.id,iduser=1)
		logging.debug("video2")
		self.op.getKeyPointsVideo(input = self.act.data["video3File"], outputV = self.act.data["videoout3File"],idAct = self.act.id,iduser=2)
		logging.debug("video3")
		self.op.getKeyPointsVideo(input = self.act.data["video4File"], outputV = self.act.data["videoout4File"],idAct = self.act.id,iduser=3)
		logging.debug("video4")
		del self.op

