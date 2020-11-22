from datetime import datetime
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
	
	def get_data(self):
		return self.data
	
	def startRecording(self):
		newvalues = { "$set": { "startRecording": datetime.today() } }
		self.mg.update_one("Activities", id = self.id, newvalues = newvalues )
	
	def endRecording(self):
		newvalues = { "$set": { "endRecording": datetime.today() } }
		self.mg.update_one("Activities", id = self.id, newvalues = newvalues )