import pyaudio
import wave

# variables del sistema
CHUNK = 480
CHANNELS = 4
RATE = 16000
FORMAT = pyaudio.paInt16

class record(object):
	def __init__(self, rootfile):
		self.rootfile = rootfile
		self.frames	= []
		self.p = pyaudio.PyAudio()
		self.wf = wave.open(self.rootfile, 'wb')
		self.wf.setnchannels(CHANNELS)
		self.wf.setsampwidth(self.p.get_sample_size(FORMAT))
		self.wf.setframerate(RATE)

	def setFrame(self, frame):
		self.frames.append(frame)
	
	def recordAudio(self):
		self.wf.writeframes(b''.join(self.frames))
		print('...')
	
	def close(self):
		self.wf.close()