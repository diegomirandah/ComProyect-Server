import sys
import cv2
import os
from sys import platform
import argparse
print("start")

try:
	# Import Openpose (Windows/Ubuntu/OSX)
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print(dir_path)
	try:
		# Windows Import
		if platform == "win32":
			print("win32")
			# Change these variables to point to the correct folder (Release/x64 etc.)
			sys.path.append(dir_path + '/../openpose/build/python/openpose/Release');
			os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../openpose/build/x64/Release;' +  dir_path + '/../openpose/build/bin;'
			import pyopenpose as op
		else:
			print("noooop")
			# Change these variables to point to the correct folder (Release/x64 etc.)
			sys.path.append('../openpose/build/python');
			# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
			# sys.path.append('/usr/local/python')
			from openpose import pyopenpose as op
	except ImportError as e:
		print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
		raise e
	
	print("Flags")
	parser = argparse.ArgumentParser()
	parser.add_argument("--image_path", default="../openpose/examples/media/COCO_val2014_000000000360.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
	args = parser.parse_known_args()

	params = dict()
	params["model_folder"] = "/models/"

	# Add others in path?
	for i in range(0, len(args[1])):
		curr_item = args[1][i]
		if i != len(args[1])-1: next_item = args[1][i+1]
		else: next_item = "1"
		if "--" in curr_item and "--" in next_item:
			key = curr_item.replace('-','')
			if key not in params:  params[key] = "1"
		elif "--" in curr_item and "--" not in next_item:
			key = curr_item.replace('-','')
			if key not in params: params[key] = next_item

	# Starting OpenPose
	print("Starting OpenPose WrapperPython")
	opWrapper = op.WrapperPython()
	print("Starting OpenPose configure")
	opWrapper.configure(params)
	print("Starting OpenPose start")
	opWrapper.start()
	print("Starting OpenPose start2")

	datum = op.Datum()
	print("Starting Datum")
	imageToProcess = cv2.imread(args[0].image_path)
	print("Starting imageToProcess")
	datum.cvInputData = imageToProcess
	print("Starting cvInputData")
	opWrapper.emplaceAndPop([datum])
	print("Starting emplaceAndPop")

	# Display Image
	print("Body keypoints: \n" + str(datum.poseKeypoints))
	cv2.imshow("OpenPose 1.6.0 - Tutorial Python API", datum.cvOutputData)
	cv2.waitKey(0)

	
except Exception as e:
	print(e)
	sys.exit(-1)