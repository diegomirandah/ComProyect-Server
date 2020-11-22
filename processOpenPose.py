#from video.OpenPoseClassPython import OPVideo
import sys
import cv2
import os
from sys import platform
from mongo import mongo
import argparse
from datetime import datetime
import datetime
from bson.objectid import ObjectId
import numpy as np

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
	# Windows Import
	if platform == "win32":
		# Change these variables to point to the correct folder (Release/x64 etc.)
		sys.path.append(dir_path + '/../build/python/openpose/Release');
		os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../build/x64/Release;' +  dir_path + '/../build/bin;'
		import pyopenpose as op
	else:
		# Change these variables to point to the correct folder (Release/x64 etc.)
		sys.path.append('../build/python');
		# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
		# sys.path.append('/usr/local/python')
		from openpose import pyopenpose as op
except ImportError as e:
	print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
	sys.exit(-1)

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--input", default="video/video1.avi", help="video de entrada")
parser.add_argument("--output", default="video/output.avi", help="video de salida")
parser.add_argument("--mode", default=False, help="intefaz grafica")
parser.add_argument("--mg", default=False, help="guardar datos")
parser.add_argument("--idAct", default=None, help="id mongo de la actividad")
parser.add_argument("--idUser", default=None, help="numero de la camara del usuario")
args = parser.parse_known_args()

params = dict()
params["model_folder"] = "../models/"
#params["face"] = True
#params["hand"] = True

class processOpenPose():
	def __init__(self, fps = 20, mg = None, mode = False):
		# Starting OpenPose
		self.opWrapper = op.WrapperPython()
		self.opWrapper.configure(params)
		self.opWrapper.start()
		self.datum = op.Datum()
		self.fourcc = "MJPG"
		self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
		self.fps = fps
		self.mg = mg
		self.mode = mode
		self.StartTime = None
		self.size = (320,240)


	def getJsonPoint(self, poseKeypoints,faceKeypoints,handLKeypoints,handRKeypoints, time = None, numFrame = None, idact = None, iduser = None):
		jp = {}
		jp["idact"] = idact
		jp["iduser"] = iduser
		jp["time"] = time
		jp["numFrame"] = numFrame
		if len(poseKeypoints) >0 :
			jp["posture"] = {
				'Nariz': None, 
				'Cuello' : None,
				'R_Hombro': None,
				'R_Codo': None,
				'R_muneca': None,
				'L_Hombro': None,
				'L_Codo': None,
				'L_muneca': None,
				'C_pelvis': None,
				'R_pelvis': None,
				'R_Rodilla': None,
				'R_Tobillo': None,
				'L_pelvis': None,
				'L_Rodilla': None,
				'L_Tobillo': None,
				'R_ojo': None,
				'L_ojo': None,
				'R_oreja': None,
				'L_oreja': None
			}
			keys = jp["posture"].keys()
			i = 0
			for key in keys:
				jp["posture"][key] = poseKeypoints[i,:2]
				i += 1
		if len(faceKeypoints) > 0:
			for key in range(70):
				jp["face"][str(key)] = faceKeypoints[i,:2]
		if len(handRKeypoints) > 0:
			for key in range(21):
				jp["handR"][str(key)] = handRKeypoints[i,:2]
		if len(handLKeypoints) >0:
			for key in range(21):
				jp["handL"][str(key)] = handLKeypoints[i,:2]
		return jp
	
	def generateVector(self, namePosture = None):
		lista = []
		if "posture" in self.jp and self.jp["posture"] != None and len(self.jp["posture"].keys())>0:
			lista = [
				np.linalg.norm(self.jp["posture"]["R_muneca"] - self.jp["posture"]["L_muneca"]),
				np.linalg.norm(self.jp["posture"]["R_muneca"] - self.jp["posture"]["R_Hombro"]),
				np.linalg.norm(self.jp["posture"]["R_muneca"] - self.jp["posture"]["Cuello"]),
				np.linalg.norm(self.jp["posture"]["R_muneca"] - self.jp["posture"]["L_Codo"]),
				np.linalg.norm(self.jp["posture"]["R_Codo"] - self.jp["posture"]["L_muneca"]),
				np.linalg.norm(self.jp["posture"]["R_Codo"] - self.jp["posture"]["R_Hombro"]),
				np.linalg.norm(self.jp["posture"]["R_Codo"] - self.jp["posture"]["L_Hombro"]),
				np.linalg.norm(self.jp["posture"]["R_Codo"] - self.jp["posture"]["Cuello"]),
				np.linalg.norm(self.jp["posture"]["R_Codo"] - self.jp["posture"]["L_Codo"]),
				np.linalg.norm(self.jp["posture"]["L_muneca"] - self.jp["posture"]["R_muneca"]),
				np.linalg.norm(self.jp["posture"]["L_muneca"] - self.jp["posture"]["L_Hombro"]),
				np.linalg.norm(self.jp["posture"]["L_muneca"] - self.jp["posture"]["Cuello"]),
				np.linalg.norm(self.jp["posture"]["L_muneca"] - self.jp["posture"]["R_Codo"]),
				np.linalg.norm(self.jp["posture"]["L_Codo"] - self.jp["posture"]["R_muneca"]),
				np.linalg.norm(self.jp["posture"]["L_Codo"] - self.jp["posture"]["R_Hombro"]),
				np.linalg.norm(self.jp["posture"]["L_Codo"] - self.jp["posture"]["L_Hombro"]),
				np.linalg.norm(self.jp["posture"]["L_Codo"] - self.jp["posture"]["Cuello"]),
				np.linalg.norm(self.jp["posture"]["Nariz"] - self.jp["posture"]["R_Hombro"]),
				np.linalg.norm(self.jp["posture"]["Nariz"] - self.jp["posture"]["L_Hombro"]),
				np.linalg.norm(self.jp["posture"]["Nariz"] - self.jp["posture"]["Cuello"]),
				np.linalg.norm(self.jp["posture"]["R_oreja"] - self.jp["posture"]["R_Hombro"]),
				np.linalg.norm(self.jp["posture"]["R_oreja"] - self.jp["posture"]["L_Hombro"]),
				np.linalg.norm(self.jp["posture"]["R_oreja"] - self.jp["posture"]["Cuello"]),
				np.linalg.norm(self.jp["posture"]["R_oreja"] - self.jp["posture"]["R_muneca"]),
				np.linalg.norm(self.jp["posture"]["R_oreja"] - self.jp["posture"]["L_muneca"]),
				np.linalg.norm(self.jp["posture"]["L_oreja"] - self.jp["posture"]["R_Hombro"]),
				np.linalg.norm(self.jp["posture"]["L_oreja"] - self.jp["posture"]["L_Hombro"]),
				np.linalg.norm(self.jp["posture"]["L_oreja"] - self.jp["posture"]["Cuello"]),
				np.linalg.norm(self.jp["posture"]["L_oreja"] - self.jp["posture"]["R_muneca"]),
				np.linalg.norm(self.jp["posture"]["L_oreja"] - self.jp["posture"]["L_muneca"]),
			]
		else:
			return None
		if namePosture != None:
			lista.append(namePosture)
		return lista

	def transform(self):
		data = {
			"idact" : self.jp["idact"],
			"iduser" : self.jp["iduser"],
			"time" : self.jp["time"],
			"timeAct" : self.timeActivitie,
			"numFrame" : self.jp["numFrame"],
			"posture" : {},
			"face" : {},
			"handR" : {},
			"handL" : {},
			"vector": []
		}
		if "posture" in self.jp:
			keys = self.jp["posture"].keys()
			for key in keys:
				data["posture"][key] = self.jp["posture"][key].tolist()
		if "face" in self.jp:
			keys = self.jp["face"].keys()
			for key in keys:
				data["face"][key] = self.jp["face"][key].tolist()
		if "handR" in self.jp:
			keys = self.jp["handR"].keys()
			for key in keys:
				data["handR"][key] = self.jp["handR"][key].tolist()
		if "handL" in self.jp:
			keys = self.jp["handL"].keys()
			for key in keys:
				data["handL"][key] = self.jp["handL"][key].tolist()	
		if "vector" in self.jp:
			for element in self.jp["vector"] or []:
				data["vector"].append(element.item())
		return data
	
	def getPoints(self):
		try:
			self.pk = self.datum.poseKeypoints[0]
		except:
			self.pk = []
		try:
			self.fk = self.datum.faceKeypoints[0]
		except:
			self.fk = []
		try:
			self.hrk = self.datum.handKeypoints[1][0]
		except:
			self.hrk = []
		try:
			self.hlk = self.datum.handKeypoints[0][0]
		except:
			self.hlk = []
		self.jp = self.getJsonPoint(
				time = self.time,
				numFrame = self.count,
				poseKeypoints = self.pk,
				faceKeypoints = self.fk,
				handLKeypoints = self.hlk,
				handRKeypoints = self.hrk,
				idact = self.idact,
				iduser = self.iduser)
		self.jp["vector"] = self.generateVector()

	
	def getKeyPointsVideo(self, input, output, idact = None, iduser = None):
		if os.path.exists(output):
			os.remove(output)
			print(f"Remove file {output}")
		if self.mg != None and idact != None:
			activitie = self.mg.find_one_atr_value("Activities","_id",idact)
			self.mg.delete_many_openpose_data(idact,iduser)
			if activitie != None:
				self.StartTime = activitie["startRecording"]
		self.idact = idact
		self.iduser = iduser
		self.count = 0
		cap = cv2.VideoCapture(input)
		video_out = cv2.VideoWriter(output, self.video_writer, self.fps, self.size)
		while (cap.isOpened()):
			hasframe, frame= cap.read()
			if hasframe == True:
				self.count += 1
				self.time = self.count/self.fps
				self.timeActivitie = self.StartTime + datetime.timedelta(seconds = self.time)
				self.datum.cvInputData = frame
				self.opWrapper.emplaceAndPop([self.datum])
				self.getPoints()
				video_out.write(self.datum.cvOutputData)
				if self.mg != None:
					self.mg.insert_one(collection = "openpose_data", data = self.transform())
				if self.mode:
					cv2.imshow("OpenPose 1.6.0", self.datum.cvOutputData)
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
			else:
				break
		video_out.release()
		cap.release()
		return

if __name__ == '__main__':
	mg = None
	ooo = None
	if args[0].mg:
		mg = mongo()
		ooo = processOpenPose(mg = mg, mode = args[0].mode)
	else:
		ooo = processOpenPose(mode = args[0].mode)
	idact = ObjectId(args[0].idAct)
	ooo.getKeyPointsVideo(input = args[0].input, output = args[0].output, idact = idact, iduser = args[0].idUser)
