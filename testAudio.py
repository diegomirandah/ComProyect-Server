from audio.audio import Audio
import threading
import logging
from datetime import datetime
import time

if __name__ == '__main__':
	ip_server = "192.168.1.128"
	portAudio = 5000
	output = "audio/outputTest.wav"
	audio = Audio(ipServer=ip_server, portAudio = portAudio, file = output, mode = False)
	audio.start()
	audio.record()
	time.sleep(20)
	audio.finished()