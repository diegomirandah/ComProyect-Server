import pymongo
from bson.objectid import ObjectId
# establing connection
try:
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

mydb = myclient["ComProyect"]
Activities = mydb["Activities"]
vad_doa = mydb["vad_doa"]
openpose = mydb["openpose_data"]
posture_close = mydb["posture_close"]

class mongo:
	def __init__(self):
		pass
		#print("mongo vive")

	def insert_one(seft,collection,data):
		return mydb[collection].insert_one(data).inserted_id

	def insert_many(seft,collection,list_data):
		return mydb[collection].insert_many(list_data)
	
	def update_one(self,collection,id,newvalues):
		myquery = { "_id": id }
		return mydb[collection].update_one(myquery, newvalues)
	
	def find_all(self,collection):
		return mydb[collection].find()
	
	def find_activities(self):
		return mydb["Activities"].find({ "$and": [{ "startRecording": { "$ne":""} },{ "endRecording": { "$ne":""} }]} )
	
	def find_all_query(self,collection,query):
		return mydb[collection].find(query)

	def find_one_atr_value(self,collection,atr,value):
		query = { atr: ObjectId(value) }
		for x in mydb[collection].find(query):
			return x
		return None
	def delete_many_openpose_data(self, idact, iduser):
		query = {"$and":[{"idact": {"$eq": ObjectId(idact)}},{"iduser": {"$eq": str(iduser)}}]}
		return mydb["openpose_data"].delete_many(query)
	
	def delete_many_postures_data(self,posture, idact, iduser):
		query = {"$and":[{"idact": {"$eq": ObjectId(idact)}},{"iduser": {"$eq": str(iduser)}}]}
		return mydb[posture].delete_many(query)

if __name__ == '__main__':
	mg = mongo()
	id_ = mg.insert_one("test",{"test":0})
	mg.insert_many("test",[{"test":0},{"test":2}])