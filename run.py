from flask import Flask, jsonify, render_template, request, abort, send_from_directory
import csv
import logging
import pandas as pd
import numpy as np
import math
from datetime import datetime
from datetime import timedelta
from mongo import mongo
#from service import service
from bson.objectid import ObjectId
import copy
from activity import activity
import os
import json
import subprocess

mg = mongo()
#s = service(mg)

app = Flask(__name__)

# API REST

# disponibilizar grabaciones
@app.route('/db/<path:path>')
def send_db(path):
	return send_from_directory('db', path)

# Procesar informacion para graficar
@app.route('/data/<act_id>')
def data(act_id):

	#Inicializar variables
	data = {}
	data["vad_doa"]= []
	data["link"]= []
	data["nodes"]= []
	data["interventions"] = []
	data["postures"] = []
	data["Keypoints"] = []
	track = None

	#OBtener valores actividad
	activitie = mg.find_one_atr_value("Activities","_id",act_id)
	#OBtener valores vad_doa
	query = { "idact": act_id }
	vad_doa = mg.find_all_query("vad_doa",query).sort("startTime")
	#print(vad_doa.count())
	newIntervention = {
		"user": None,
		"start": None,
		"end": None,
		"time": None,
	}
	

	for x in vad_doa:
		
		duration = x["endTime"] - x["startTime"]
		
		# crear nodo
		for n in data["nodes"]:
			if n["name"] == f"Usuario {x['micPos']+1}":
				arr = [pd.to_timedelta(n["duration"]), duration]
				n["duration"] = str(sum(arr,timedelta(0,0)))
				break
		else:
			newNode = {
				"name": f"Usuario {x['micPos']+1}",
				"interventions": 0,
				"duration": str(duration)
			}
			#print(newNode)
			data["nodes"].append(newNode)

		# crear links y intervenciones
		if track == None:
			track = f"Usuario {x['micPos']+1}"
			newIntervention["user"] = track
			newIntervention["micPos"] = x['micPos']
			newIntervention["start"] = str(x["startTime"])
			newIntervention["end"] = str(x["endTime"])
			newIntervention["time"] = str(duration)
			#ewIntervention["time_s"] = (x["endTime"] - x["startTime"]).total_seconds()
			for n in data["nodes"]:
				if n["name"] == f"Usuario {x['micPos']+1}":
					n["interventions"] = n["interventions"] + 1 
			#print(f"init tack: {track}")
		if track != None:
			if track == f"Usuario {x['micPos']+1}":
				#print(f"m source: {track} target: Usuario {x['micPos']+1}")
				arr = [pd.to_timedelta(newIntervention["time"]), duration]
				newIntervention["time"] = str(sum(arr,timedelta(0,0)))
				newIntervention["end"] = str(x["endTime"])
				newIntervention["time_s"] = (x["endTime"] - x["startTime"]).total_seconds()
				#newIntervention["time_s"] = str(sum([pd.to_timedelta(newIntervention["start"]), pd.to_timedelta(newIntervention["end"])],datetime.timedelta(0,0))).total_seconds()
			else:
				for n in data["nodes"]:
					if n["name"] == f"Usuario {x['micPos']+1}":
						n["interventions"] = n["interventions"] + 1 
				data["interventions"].append(copy.copy(newIntervention))
				newIntervention["user"] = f"Usuario {x['micPos'] + 1 }"
				newIntervention["micPos"] = x['micPos']
				newIntervention["start"] = str(x["startTime"])
				newIntervention["end"] = str(x["endTime"])
				newIntervention["time"] = str(duration)
				#newIntervention["time_s"] = str(sum([pd.to_timedelta(newIntervention["start"]), pd.to_timedelta(newIntervention["end"])],datetime.timedelta(0,0))).total_seconds()
				#print(f"c source: {track} target: Usuario {x['micPos']+1}")
				for l in data["link"]:
					if l["source"] == track and l["target"] == f"Usuario {x['micPos']+1}":
						l["sizeLink"] = l["sizeLink"] + 1
						break
				else:
					newlink = {
						"source": track,
						"target": f"Usuario {x['micPos']+1}",
						"sizeLink": 1
					}
					#print(newlink)
					data["link"].append(newlink)
				track = f"Usuario {x['micPos']+1}"
		
		#estandariza datos a norma ISO y elimina excepcion de objertId de mongodb
		x["duration"] = str(duration)
		x["startTime"] = x["startTime"].isoformat()
		x["endTime"] = x["endTime"].isoformat()
		
		x.pop('_id')
		x.pop('idact')

		#agrega elemento a respuesta
		data["vad_doa"].append(x)
		
	data["interventions"].append(copy.copy(newIntervention))

	data["dataposture"] = {}

	#OBtener valores posturas
	postures = []
	for i in range(1,5):
		query2 = { "idact": ObjectId(act_id), "iduser": str(i)}
		user = {
			"user":f"Usuario {str(i)}",
			"postures":[],
			"data": {}
		}
		for posture in mg.find_all_query("postures",query2).sort("start_s"):
			#print(f"{posture["end_s"]} - {posture["start_s"]}")
			if (float(posture["end_s"]) - float(posture["start_s"])) > 1:
				user["postures"].append({
					"start": str(posture["start"]),
					"end": str(posture["end"]),
					"start_s": posture["start_s"],
					"end_s": posture["end_s"],
					"posture": posture["posture"]
				})
				time =  float(posture["end_s"]) - float(posture["start_s"])
				user["data"][posture["posture"]] = time + float(user["data"].get(posture["posture"]) or 0)
				data["dataposture"][posture["posture"]] = time + float(data["dataposture"].get(posture["posture"]) or 0)
		postures.append(user)
	data["postures"] = postures

	""" #OBtener valores keypoints
	keypoints = []
	for i in range(1,5):
		query2 = { "idact": ObjectId(act_id), "iduser": str(i)}
		user = {
			"user":f"Usuario {str(i)}",
			"keypoints":[]
		}
		for keypoint in mg.find_all_query("openpose_data",query2).sort("numFrame"):
			user["keypoints"].append({
				"face": keypoint["face"],
				"handR": keypoint["handR"],
				"handL": keypoint["handL"],
				"vector": keypoint["vector"],
				"posture": keypoint["posture"],
				"numFrame": keypoint["numFrame"],
				"timeAct": str(keypoint["timeAct"]),
				"time": keypoint["time"],
			})
		keypoints.append(user)
	data["Keypoints"] = keypoints """
	
	# 
	activitie["id"] = act_id
	activitie.pop('_id')
	activitie["startRecording"] = str(activitie["startRecording"])
	activitie["endRecording"] = str(activitie["endRecording"])
	activitie["creationTime"] = str(activitie["creationTime"])
	data["activitie"] = activitie

	def myFunc(e):
		return (e['name'])

	data["nodes"].sort(key=myFunc)
	return jsonify(data)

# obtener datos de todas las actividades grabadas
@app.route('/get_activities_data')
def get_activities_data():
	activities = []
	for x in mg.find_all("Activities"):
		if x["startRecording"] != None and x["endRecording"] != None:
			x["id"] = str(x["_id"])
			x.pop('_id')
			activities.append(x)
	return jsonify(activities)

# Vista nueva actividada
@app.route('/new_activity/new')
def new_activity():
	return render_template('newactivitie.html')

# configurar actividad
@app.route('/new_activity/config', methods=['POST'])
def new_activity_config():
	if request.method == 'POST':
		NombreActividad = request.form['name']
		time_ = request.form['durationOfActivity']
		root = 'db/'+ datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
		os.makedirs(root, exist_ok=True)
		act = activity(root, mg, NombreActividad, time_)
		return jsonify(act.get_data())
	abort(404, description="Resource not found")

def run(cmd):
	proc = subprocess.Popen(cmd,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
	)
	stdout, stderr = proc.communicate()
	return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8")

# inicia grabacion
@app.route('/new_activity/start', methods=['POST'])
def new_activity_start():
	if request.method == 'POST':
		data_act = request.form['data_act']
		print(data_act)
		comand = ["python","./daemonRecord.py","start",data_act]
		code, out, err = run(comand)
		mensaje = {
			"out": out,
			"err":err,
			"code":code,
		}
		return jsonify(mensaje)
	abort(404, description="Resource not found")

# detener grabacion
@app.route('/new_activity/stop', methods=['POST'])
def new_activity_stop():
	if request.method == 'POST':
		data_act = request.form['data_act']
		comand = ["python","./daemonRecord.py","stop",data_act]
		code, out, err = run(comand)
		mensaje = {
			"out": out,
			"err":err,
			"code":code,
		}
		return jsonify(mensaje)
	abort(404, description="Resource not found")

# finalizar grabacion
@app.route('/new_activity/end', methods=['POST'])
def new_activity_end():
	if request.method == 'POST':
		comand = ["python","./daemonRecord.py","end"]
		code, out, err = run(comand)
		mensaje = {
			"out": out,
			"err":err,
			"code":code,
		}
		return jsonify(mensaje)
	abort(404, description="Resource not found")

# test grabacion
@app.route('/new_activity/test', methods=['POST'])
def new_activity_test():
	if request.method == 'POST':
		data_act = request.form['data_act']
		comand = ["python","./daemonRecord.py","child",data_act]
		subprocess.run(comand)
		return jsonify("testing")
	abort(404, description="Resource not found")

# Processar video con openpose
@app.route('/processOpenPose', methods=['POST'])
def processVideo():
	if request.method == 'POST':
		comand = [
			"python",
			"./processOpenPose.py",
			"--input=" + str(request.form['input']), 
			"--output=" + str(request.form['output']),
			"--mg=True",
			"--idAct="+ str(request.form['act_id']),
			"--idUser="+ str(request.form['user_id'])]
		subprocess.run(comand)
		return jsonify("processVideo")
	abort(404, description="Resource not found")

# Generar Posturas
@app.route('/processPostures', methods=['POST'])
def processPostures():
	if request.method == 'POST':
		comand = [
			"python",
			"./processPostures.py",
			"--idAct="+ str(request.form['act_id']),
			"--idUser="+ str(request.form['user_id'])]
		subprocess.run(comand)
		return jsonify("processVideo")
	abort(404, description="Resource not found")

# Pagina de inicio
@app.route('/')
def index():
	acts = mg.find_activities()
	return render_template('index.html', activities = enumerate(acts))

# Vista de una actividad
@app.route('/act/<act_id>')
def act(act_id):
	act = mg.find_one_atr_value("Activities","_id", act_id)
	return render_template('dashboard.html', activity = act)
		
if __name__ == '__main__':
	  app.run(host= '192.168.1.128',debug=True)