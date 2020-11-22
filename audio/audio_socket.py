import pyaudio
import socket
import threading
import numpy as np

class AudioSocket(object):
	def __init__(self, ipServer, portAudio = 5000):
		#variables
		self.ip_server = ipServer
		self.portAudio = portAudio
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1 
		self.RATE = 16000
		self.CHUNK = 480
		
		#feedback
		print("Start Audio")
		print("IP_SERVER ",self.ip_server,self.portAudio)

		#Iniciando audio
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(
			format = self.FORMAT,
			start = False,
			channels = self.CHANNELS,
			rate = self.RATE,
			output = True,
			frames_per_buffer = self.CHUNK)

		#Iniciando socket
		self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
		self.sock.bind( (self.ip_server,self.portAudio) )

	def read_chunks(self):
		while True:
			data = self.sock.recv(100000)
			#print(data)
			frame = np.fromstring(data, dtype='int16')
			#print(len(frame[::4]))
			data2 = frame[::4].tostring()
			self.stream.write(data2, self.CHUNK) #solo se reproduce 1 canal
			yield data # se envia los 4 canales

	def start(self):
		self.stream.start_stream()
	
	def stop(self):
		self.sock.close()
		self.stream.stop_stream()
	
	def __enter__(self):
		self.start()
		return self

	def __exit__(self, type, value, traceback):
		if value:
			return False
		self.stop()

def test_audio_transmission():
	import signal
	is_quit = threading.Event()

	ip_server = "192.168.1.128"
	portAudio = 5000

	def signal_handler(sig, num):
		is_quit.set()
		print('Quit')

	signal.signal(signal.SIGINT, signal_handler)

	with AudioSocket(ip_server,portAudio) as mic:
		print("-----")
		for chunk in mic.read_chunks():
			print("*")
			if is_quit.is_set():
				break
		print("-----")

if __name__ == '__main__':
	test_audio_transmission()