from audio.gcc_phat import gcc_phat
import webrtcvad
import numpy as np
import logging
import math

vad = webrtcvad.Vad(3)
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

# variables del sistema
CHUNK = 480
CHANNELS = 4
RATE = 16000
SOUND_SPEED = 343.2
MIC_DISTANCE_4 = 0.08127
MAX_TDOA_4 = MIC_DISTANCE_4 / float(SOUND_SPEED)

class vadDoa(object):
	def __init__(self):
		self.chunks = []
		self.doa_chunks = 10
		vad = webrtcvad.Vad(3)
	
	def setChunks(self, chucks): #buffer de audio 
		self.chunks = chucks
	
	def get_direction(self, buf): # determina la direccion del sonido utilizando gcc_phat
		best_guess = None
		MIC_GROUP_N = 2
		MIC_GROUP = [[0, 2], [1, 3]]

		tau = [0] * MIC_GROUP_N
		theta = [0] * MIC_GROUP_N
		for i, v in enumerate(MIC_GROUP):
			tau[i], _ = gcc_phat(buf[v[0]::4], buf[v[1]::4], fs=RATE, max_tau=MAX_TDOA_4, interp=1)
			theta[i] = math.asin(tau[i] / MAX_TDOA_4) * 180 / math.pi

		if np.abs(theta[0]) < np.abs(theta[1]):
			if theta[1] > 0:
				best_guess = (theta[0] + 360) % 360
			else:
				best_guess = (180 - theta[0])
		else:
			if theta[0] < 0:
				best_guess = (theta[1] + 360) % 360
			else:
				best_guess = (180 - theta[1])
			best_guess = (best_guess + 90 + 180) % 360
		return best_guess
	
	def get_vad(self, chunk): #determina si el sonido es voz o ruido ambiente
		if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
			return 1
		else:
			return 0

	def get_voa_doa(self): #determina si el buffer de audio contiene voz y supera umbral para determinar direccion del sonido
		micPos = None
		direction = None
		self.speech_count = 0
		for chuck in self.chunks:
			self.speech_count += self.get_vad(chuck)
		if self.speech_count > (self.doa_chunks / 3):
			frames = np.concatenate(self.chunks)
			direction = self.get_direction(frames)
			#print('Direccion: {}'.format(int(direction)))
			if int(direction) < 90:
				micPos = 0
			elif int(direction) < 180:
				micPos = 1
			elif int(direction) < 270:
				micPos = 2
			else:
				micPos = 3
		return self.speech_count, micPos, direction
		
