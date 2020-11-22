import sys
from mongo import mongo
import argparse
from datetime import datetime
import datetime
from bson.objectid import ObjectId
from tensorflow.keras.models import Sequential, load_model
import numpy as np
import tensorflow as tf
import math

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--modelpath", default='models/softmax_adamax_hands_together.h5', help="modelo")
parser.add_argument("--idAct", help="id mongo de la actividad")
parser.add_argument("--idUser", help="numero de la camara del usuario")
args = parser.parse_known_args()

class processPosture():
	def __init__(self, mg, modelpath):
		self.mg = mg
		self.modelpath = modelpath
		self.StartTime = None
		self.model = load_model('models/softmax_adamax_hands_together.h5')

	def get_data(self, idact,iduser):
		query = { "idact": ObjectId(idact), "iduser": str(iduser)}
		return self.mg.find_all_query("openpose_data",query).sort("time")
	
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

	def classifyPosture(self, vector):
		if vector != None and vector != []:
			prediction = self.model.predict(tf.constant([vector]))
			num = np.argmax(prediction)
			return self.posture_mg(num), prediction.item(num)
		else:
			return None, None
	
	def registerPosture(self, posture, data):
		data["start"] = self.StartTime + datetime.timedelta(seconds = data["start_s"])
		data["end"] = self.StartTime + datetime.timedelta(seconds = data["end_s"])
		data["posture"] = posture
		self.mg.insert_one(collection = "postures", data = data)
	
	def deleteData(self, idact, iduser):
		for num in range(10):
			self.mg.delete_many_postures_data(self.posture_mg(num), idact, iduser)
	
	def processData(self, idact, iduser ):
		activitie = self.mg.find_one_atr_value("Activities","_id",idact)
		if activitie != None and int(iduser) in range(1,5):
			self.deleteData(idact,iduser)
			self.StartTime = activitie["startRecording"]
			trace = None
			data = {
				"iduser": iduser,
				"idact": ObjectId(idact),
				"start_s": None,
				"end_s": None
			}
			for frame in self.get_data(idact,iduser):
				data["_id"] = ObjectId()
				posture, probability = self.classifyPosture(frame["vector"])
				if posture != None:
					if trace == None:
						trace = posture
						data["start_s"] = frame["time"]
						data["end_s"] = frame["time"]
					if posture != trace:
						time = frame["time"]
						data["end_s"] = frame["time"]
						#print("change trace", trace, posture, data["start_s"], data["end_s"])
						self.registerPosture(posture = trace, data = data)
						trace = posture
						data["start_s"] = frame["time"]

		


if __name__ == '__main__':
	mg = mongo()
	ooo = processPosture(mg = mg, modelpath = args[0].modelpath)
	ooo.processData(idact = args[0].idAct, iduser = args[0].idUser)
