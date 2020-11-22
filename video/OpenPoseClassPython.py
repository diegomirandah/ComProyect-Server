# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
from datetime import datetime
from bson.objectid import ObjectId
import numpy as np
import csv
from tensorflow.keras.models import Sequential, load_model
import tensorflow as tf

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
	# Windows Import
	if platform == "win32":
		# Change these variables to point to the correct folder (Release/x64 etc.)
		sys.path.append(dir_path + '/../../build/python/openpose/Release');
		os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../build/x64/Release;' +  dir_path + '/../../build/bin;'
		import pyopenpose as op
	else:
		# Change these variables to point to the correct folder (Release/x64 etc.)
		sys.path.append('../../build/python');
		# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
		# sys.path.append('/usr/local/python')
		from openpose import pyopenpose as op
except ImportError as e:
	print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
	sys.exit(-1)

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--mongo", default=False, help="Registrar en MongoDb")
parser.add_argument("--mode", default=False, help="feedback de video")
parser.add_argument("--input", default="video/video1.avi", help="video de entrada")
parser.add_argument("--outputVideo", default="video/output.avi", help="video de salida")
parser.add_argument("--fileOutput", default=None, help="archivo de salida")
parser.add_argument("--namePosture", default=None, help="nombre postura")
parser.add_argument("--data", default="video/data.dat", help="datos de keypoints")
parser.add_argument("--idAct", default=None, help="id mongo de la actividad")
parser.add_argument("--idUser", default=None, help="numero de la camara del usuario")
args = parser.parse_known_args()

params = dict()
params["model_folder"] = "../models/"
params["face"] = True
params["hand"] = True


jPoint = {
	"_id":"ddd",
	"idact": "ddd",
	"time": "time",
	"numFrame": 0,
	"posture": {
	},
	"face":{
	},
	"handR":{
	},
	"handL":{
	}
}

# font 
font = cv2.FONT_HERSHEY_SIMPLEX
# org 
org = (0, 50)
# fontScale 
fontScale = 0.5
# Blue color in BGR 
color = (255, 0, 0)

postures = [
"Crossing_arms_left",
"Crossing_arms_right",
"hands_hip",
"hands_to_head",
"hug_opposite_arm_left",
"hug_opposite_arm_right",
"Scratching_your_neck_left",
"Scratching_your_neck_right",
"normal_posture",
"hands_togethe"
]

class OPVideo():
	def __init__(self, fps = 20, mg = None, mode = False):
		# Starting OpenPose
		self.opWrapper = op.WrapperPython()
		self.opWrapper.configure(params)
		self.opWrapper.start()
		self.datum = op.Datum()
		self.fourcc = "MJPG"
		self.fps = fps
		self.mg = mg
		self.mode = mode
		self.model = load_model('models/softmax_adamax_hands_together.h5')
		
	
	def getJsonPoint(self, poseKeypoints,faceKeypoints,handLKeypoints,handRKeypoints, time = None, numFrame = None, idact = None, iduser = None):
		jp = jPoint
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

	def transform(self, jp):
		data = {
			"idact" : jp["idact"],
			"iduser" : jp["iduser"],
			"time" : jp["time"],
			"numFrame" : jp["numFrame"],
			"posture" : {},
			"face" : {},
			"handR" : {},
			"handL" : {},
		}
		keys = jp["posture"].keys()
		for key in keys:
			data["posture"][key] = jp["posture"][key].tolist()
		keys = jp["face"].keys()
		for key in keys:
			data["face"][key] = jp["face"][key].tolist()
		keys = jp["handR"].keys()
		for key in keys:
			data["handR"][key] = jp["handR"][key].tolist()
		keys = jp["handL"].keys()
		for key in keys:
			data["handL"][key] = jp["handL"][key].tolist()
		return data
	
	def generateVector(self, jp, namePosture=None):
		lista = []
		if jp["posture"] != None and len(jp["posture"].keys())>0:
			lista = [
				np.linalg.norm(jp["posture"]["R_muneca"] - jp["posture"]["L_muneca"]),
				np.linalg.norm(jp["posture"]["R_muneca"] - jp["posture"]["R_Hombro"]),
				np.linalg.norm(jp["posture"]["R_muneca"] - jp["posture"]["Cuello"]),
				np.linalg.norm(jp["posture"]["R_muneca"] - jp["posture"]["L_Codo"]),
				np.linalg.norm(jp["posture"]["R_Codo"] - jp["posture"]["L_muneca"]),
				np.linalg.norm(jp["posture"]["R_Codo"] - jp["posture"]["R_Hombro"]),
				np.linalg.norm(jp["posture"]["R_Codo"] - jp["posture"]["L_Hombro"]),
				np.linalg.norm(jp["posture"]["R_Codo"] - jp["posture"]["Cuello"]),
				np.linalg.norm(jp["posture"]["R_Codo"] - jp["posture"]["L_Codo"]),
				np.linalg.norm(jp["posture"]["L_muneca"] - jp["posture"]["R_muneca"]),
				np.linalg.norm(jp["posture"]["L_muneca"] - jp["posture"]["L_Hombro"]),
				np.linalg.norm(jp["posture"]["L_muneca"] - jp["posture"]["Cuello"]),
				np.linalg.norm(jp["posture"]["L_muneca"] - jp["posture"]["R_Codo"]),
				np.linalg.norm(jp["posture"]["L_Codo"] - jp["posture"]["R_muneca"]),
				np.linalg.norm(jp["posture"]["L_Codo"] - jp["posture"]["R_Hombro"]),
				np.linalg.norm(jp["posture"]["L_Codo"] - jp["posture"]["L_Hombro"]),
				np.linalg.norm(jp["posture"]["L_Codo"] - jp["posture"]["Cuello"]),
				np.linalg.norm(jp["posture"]["Nariz"] - jp["posture"]["R_Hombro"]),
				np.linalg.norm(jp["posture"]["Nariz"] - jp["posture"]["L_Hombro"]),
				np.linalg.norm(jp["posture"]["Nariz"] - jp["posture"]["Cuello"]),
				np.linalg.norm(jp["posture"]["R_oreja"] - jp["posture"]["R_Hombro"]),
				np.linalg.norm(jp["posture"]["R_oreja"] - jp["posture"]["L_Hombro"]),
				np.linalg.norm(jp["posture"]["R_oreja"] - jp["posture"]["Cuello"]),
				np.linalg.norm(jp["posture"]["R_oreja"] - jp["posture"]["R_muneca"]),
				np.linalg.norm(jp["posture"]["R_oreja"] - jp["posture"]["L_muneca"]),
				np.linalg.norm(jp["posture"]["L_oreja"] - jp["posture"]["R_Hombro"]),
				np.linalg.norm(jp["posture"]["L_oreja"] - jp["posture"]["L_Hombro"]),
				np.linalg.norm(jp["posture"]["L_oreja"] - jp["posture"]["Cuello"]),
				np.linalg.norm(jp["posture"]["L_oreja"] - jp["posture"]["R_muneca"]),
				np.linalg.norm(jp["posture"]["L_oreja"] - jp["posture"]["L_muneca"]),
			]
		else:
			return None
		if namePosture != None:
			lista.append(namePosture)
		return lista
	
	def clasificarPostura(self, puntos):
		if puntos != None:
			self.model = load_model('models/softmax_adamax_hands_together.h5')
			prediction = self.model.predict(tf.constant([puntos]))
			num = np.argmax(prediction)
			return num, prediction.item(num)
		else:
			return None, None

	def posture_mg(self, num_posture):
		switcher={
				0:'posture_close',
				1:'posture_close',
				2:'posture_hands_hip',
				3:'posture_hands_to_head',
				4:'posture_hug_opposite_arm',
				5:'posture_hug_opposite_arm',
				6:'posture_scratching_your_neck',
				7:'posture_scratching_your_neck',
				8:'posture_normal',
				9:'posture_hands_together',
			 }
		return switcher.get(num_posture,None)

	def postures(self,frame, jp):
		num_posture, acc_posture = self.clasificarPostura(self.generateVector(jp))
		#print(self.posture_mg(num_posture), acc_posture)
		frame = cv2.putText(frame, self.posture_mg(num_posture), (0, 30) , font, fontScale, color)
		if self.mg != None:
			jp["_id"] = ObjectId()
			self.mg.insert_one(collection="openpose_data",data=self.transform(jp))
			if num_posture != 8 and num_posture != None:
				self.mg.insert_one(self.posture_mg(num_posture),{
						"_id" : ObjectId(),
						"idact": self.idact,
						"iduser": self.iduser,
						"time": self.time,
						"count": self.count
					})
		return frame

	def getKeyPointsVideo(self, input, outputV, idact = None, iduser = None):
		self.idact = idact
		self.iduser = iduser
		cap = cv2.VideoCapture(input)
		video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
		video_out = cv2.VideoWriter(outputV, video_writer, self.fps, (320,240))
		self.count = 0
		while (cap.isOpened()):
			hasframe, frame= cap.read()
			if hasframe== True:
				self.datum.cvInputData = frame
				self.count+=1
				self.opWrapper.emplaceAndPop([self.datum])
				try:
					pk = self.datum.poseKeypoints[0]
				except:
					pk = []
				try:
					fk = self.datum.faceKeypoints[0]
				except:
					fk = []
				try:
					hrk = self.datum.handKeypoints[1][0]
				except:
					hrk = []
				try:
					hlk = self.datum.handKeypoints[0][0]
				except:
					hlk = []
				self.time = self.count/self.fps
				jp = self.getJsonPoint(
					time = self.time,
					numFrame = self.count,
					poseKeypoints = pk,
					faceKeypoints = fk,
					handLKeypoints = hlk,
					handRKeypoints = hrk,
					idact = idact,
					iduser = iduser)
				
				self.datum.cvOutputData = self.postures(frame = self.datum.cvOutputData, jp=jp)
				video_out.write(self.datum.cvOutputData)
				if self.mode:
					#print(jp)
					cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", self.datum.cvOutputData)
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
			else:
				break
		video_out.release()
		cap.release()
		return
	
	def GetCsv(self, input, outputV, fileOutput, namePosture):
		cap = cv2.VideoCapture(input)
		fps = cap.get(cv2.CAP_PROP_FPS)
		video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
		video_out = cv2.VideoWriter(outputV, video_writer, fps, (320,240))
		with open(fileOutput, 'w', newline='') as csvfile:
			salida = csv.writer(csvfile, delimiter=";" , quotechar='"', quoting=csv.QUOTE_MINIMAL)
			#salida.writerow(['campo1', 'campo2'])
			
			while (cap.isOpened()):
				hasframe, frame= cap.read()
				if hasframe == True:
					self.datum.cvInputData = frame
					self.opWrapper.emplaceAndPop([self.datum])
					try:
						pk = self.datum.poseKeypoints[0]
					except:
						pk = []
					try:
						fk = self.datum.faceKeypoints[0]
					except:
						fk = []
					try:
						hrk = self.datum.handKeypoints[1][0]
					except:
						hrk = []
					try:
						hlk = self.datum.handKeypoints[0][0]
					except:
						hlk = []
					jp = self.getJsonPoint(
						poseKeypoints = pk,
						faceKeypoints = fk,
						handLKeypoints = hlk,
						handRKeypoints = hrk)
					salida.writerows([self.generateVector(jp,namePosture)])
					video_out.write(self.datum.cvOutputData)
					if self.mode:
						#print(jp)
						cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", self.datum.cvOutputData)
						if cv2.waitKey(1) & 0xFF == ord('q'):
							break
				else:
					break
		del salida
		csvfile.close()
		video_out.release()
		cap.release()
		return


if __name__ == '__main__':
	ooo = OPVideo(mode=args[0].mode)
	ooo.getKeyPointsVideo( input = args[0].input, outputV = args[0].outputVideo, idact = args[0].idAct, iduser = args[0].idUser)
	#ooo.GetCsv(args[0].input,args[0].outputVideo,args[0].fileOutput, args[0].namePosture)
