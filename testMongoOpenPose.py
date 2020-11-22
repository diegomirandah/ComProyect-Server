from video.OpenPoseClassPython import OPVideo
from mongo import mongo
import argparse
from bson.objectid import ObjectId

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--input", default="video/video1.avi", help="video de entrada")
parser.add_argument("--outputVideo", default="video/output.avi", help="video de salida")
parser.add_argument("--mode", default=False, help="intefaz grafica")
parser.add_argument("--mg", default=False, help="guardar datos")
args = parser.parse_known_args()

if __name__ == '__main__':
	mg = mongo()
	ooo = None
	if args[0].mg:
		ooo = OPVideo(mg = mg, mode = args[0].mode)
	else:
		ooo = OPVideo(mode = args[0].mode)
	idact = ObjectId()
	ooo.getKeyPointsVideo(input = args[0].input,outputV = args[0].outputVideo, idact = idact,iduser = 0)