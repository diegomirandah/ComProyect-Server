from video.video import Video
import threading
import logging
from datetime import datetime
import time

if __name__ == '__main__':
	ip_server = "192.168.1.128"
	port = 5003
	output = "dataset/test.avi"
	video = Video(ipServer=ip_server, port = port, file = output, mode = True)
	print("start")
	video.start()
	time.sleep(10)
	#print("record")
	#video.record()
	time.sleep(200)
	#print("finished")
	video.finished()
