import threading
import logging
from datetime import datetime
from audio.audio_socket import AudioSocket
from audio.vad_doa import vadDoa
#from audio.vokaturi.Emotion	import Emotion
#from audio.audio_data import audioData
from audio.record import record
import numpy as np
#import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class Audio(threading.Thread):
	def __init__(self, ipServer, file, mg = None, idAct = None, portAudio = 5000, mode = True):
		threading.Thread.__init__(self)
		self.ipServer = ipServer
		self.portAudio = portAudio
		self._running = True
		self.vad_doa = vadDoa() # iniciar detector de voz y direccion
		#self.emotion = Emotion(16000,14400) # inciar detector de emocion
		self.file = file
		self.R = record(self.file)
		self.rec = False
		self.mg = mg
		self.idAct = idAct
		self.mode = mode
		logging.debug('Start Audio in port: ' + str(self.portAudio))
	
	def record(self):
		self.rec = True
	
	def finished(self):
		print("save")
		self.R.recordAudio()
		self._running = False
		self.rec = False
	
	# def register_emotion(self, emotion):
	# 	data = {
	# 		"idact": self.idAct,
	# 		"dateTime": datetime.today(),
	# 		"vad_doa": self.id_,
	# 		"Happiness": emotion.happiness,
	# 		"Neutral" : emotion.neutrality,
	# 		"Sadness" : emotion.sadness,
	# 		"Fear" : emotion.fear,
	# 		"Anger" : emotion.anger
	# 	}
	# 	if self.mode:
	# 		self.id_ = self.mg.insert_one("vokaturi_emotion",data)

	def register_vad_doa(self,speech_count, startTime, endTime, micPos, direction, emotion = None):
		data = {
			"idact": self.idAct,
			"startTime": startTime,
			"endTime": endTime,
			"speech_count": speech_count,
			"micPos": micPos,
			"direction": direction
		}
		if self.mode:
			self.id_ = self.mg.insert_one("vad_doa",data)
		#print(id_)
		
	def run(self):
		logging.debug('running')
		chunks = []
		start = None
		end = None
		#chunks2 = []
		with AudioSocket(self.ipServer,self.portAudio) as mic:
			for chunk in mic.read_chunks():
				if len(chunks) == 0:
					start = datetime.today()
				frame = np.fromstring(chunk, dtype='int16')
				chunks.append(frame)
				if self.rec == True:
					self.R.setFrame(chunk)
				# chunks2.append(frame)
				if len(chunks) == 10:
					end = datetime.today()
					#determinar si hablan y quien habla
					self.vad_doa.setChunks(chunks)
					speech_count, micPos, direction = self.vad_doa.get_voa_doa()
					#logging.debug(f" speech_count {speech_count} micPos {micPos} direction {direction}")
					# registra datos en mongo
					if (self.rec == True) and micPos != None:
						self.register_vad_doa(startTime = start, endTime = end, speech_count = speech_count, micPos = micPos, direction = direction)
						
					# reinicia buffer fragmento
					chunks = []
				if self._running == False:
					break
		
		
