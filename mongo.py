import pymongo
from bson.objectid import ObjectId
# establing connection

class mongo:
	def __init__(self, host="localhost", port = 27017):
		self.host = host
		self.port = port
		try:
			self.myclient = pymongo.MongoClient(f"mongodb://{self.host}:{self.port}/")
			print("Connected successfully!!!")
		except:
			print("Could not connect to MongoDB")
		self.mydb = self.myclient["ComProyect"]
		self.Activities = self.mydb["Activities"]
		self.vad_doa =self. mydb["vad_doa"]
		self.openpose = self.mydb["openpose_data"]
		self.posture_close = self.mydb["posture_close"]

	def insert_one(self,collection,data):
		return self.mydb[collection].insert_one(data).inserted_id

	def insert_many(self,collection,list_data):
		return self.mydb[collection].insert_many(list_data)
	
	def update_one(self,collection,id,newvalues):
		myquery = { "_id": id }
		return self.mydb[collection].update_one(myquery, newvalues)
	
	def find_all(self,collection):
		return self.mydb[collection].find()
	
	def find_activities(self):
		return self.mydb["Activities"].find({ "$and": [{ "startRecording": { "$ne":""} },{ "endRecording": { "$ne":""} }]} )
	
	def find_all_query(self,collection,query):
		return self.mydb[collection].find(query)

	def find_one_atr_value(self,collection,atr,value):
		query = { atr: ObjectId(value) }
		for x in self.mydb[collection].find(query):
			return x
		return None
	def delete_many_openpose_data(self, idact, iduser):
		query = {"$and":[{"idact": {"$eq": ObjectId(idact)}},{"iduser": {"$eq": str(iduser)}}]}
		return self.mydb["openpose_data"].delete_many(query)
	
	def delete_many_postures_data(self,posture, idact, iduser):
		query = {"$and":[{"idact": {"$eq": ObjectId(idact)}},{"iduser": {"$eq": str(iduser)}}]}
		return self.mydb[posture].delete_many(query)

if __name__ == '__main__':
	mg = mongo()
	id_ = mg.insert_one("test",{"test":0})
	mg.insert_many("test",[{"test":0},{"test":2}])