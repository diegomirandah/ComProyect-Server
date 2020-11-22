import threading
import logging
import time
import cv2
import socket
import numpy as np

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class Video(threading.Thread):
	def __init__(self, ipServer, port, file, fps = 20, mode = False):
		threading.Thread.__init__(self)
		self.ipServer = ipServer
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
		self.sock.bind((self.ipServer, self.port))

		#self._running = True
		self.protocol = "udp"
		self.url = str(self.protocol) + "://" + str(self.ipServer) + ":" + str(self.port)
		#self.cap = cv2.VideoCapture("output.avi")
		logging.debug('Start Video in port: ' + self.url)
		self.open = True
		self.rec = False
		self.device_index = 0
		self.fps = fps             # fps should be the minimum constant rate at which the camera can
		self.fourcc = "MJPG"       # capture images (with no decrease in speed over time; testing is required)
		self.frameSize = (320,240) # video formats and sizes also depend and vary according to the camera used
		self.video_filename = file
		#self.video_cap = cv2.VideoCapture(self.url,cv2.CAP_FFMPEG)
		self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
		self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
		self.frame_counts = 1
		self.start_time = time.time()
		self.mode = mode
	
	def record(self):
		self.rec=True

	def finished(self): 
		if self.open==True:
			self.open=False
			self.rec=False
			self.video_out.release()
			#self.video_cap.release()
			#cv2.destroyAllWindows()
		else: 
			pass
	
	def run(self):
		#counter = 1
		while(self.open==True):
			#print("-")
			data, addr = self.sock.recvfrom(65507)
			nparr = np.fromstring(data, np.uint8)
			frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			if (self.rec == True):
				self.video_out.write(frame)
			if self.mode:
				cv2.imshow('image', frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

if __name__ == '__main__':
	ip_server = "192.168.1.128"
	port = 5004
	output = "dataset/record.avi"
	video = Video(ipServer=ip_server, port = port, file = output, mode = True)
	print("start")
	video.start()
	time.sleep(10)
	print("record")
	video.record()
	time.sleep(120)
	print("finished")
	video.finished()

