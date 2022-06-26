#!/usr/bin/env python

from wsgiref import simple_server
from flask import Flask, request, render_template, send_from_directory
from flask import Response
import os
import shutil
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        files = request.files.getlist('files')

        folderName = 'PredictionFiles'
        if os.path.isdir(folderName):
            shutil.rmtree(folderName)
        os.mkdir(folderName)

        for file in files:
            file.save(os.path.join(folderName, file.filename))

        pred_val = pred_validation(folderName)  # object initialization

        pred_val.prediction_validation()  # calling the prediction_validation function

        pred = prediction(folderName)

        # predicting for dataset present in database
        path = pred.predictionFromModel()

        return send_from_directory(path, filename= "predictions.csv", as_attachment=True)

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

# With Change in index.html we can train model on new files

# @app.route("/train", methods=['GET', 'POST'])
# @cross_origin()
# def trainRouteClient():
#
#     try:
#         # if request.json['folderPath'] is not None:
#         folder_path = "Training_Batch_Files"
#         # path = request.json['folderPath']
#         if folder_path is not None:
#             path = folder_path
#
#             train_valObj = train_validation(path)  # object initialization
#
#             train_valObj.train_validation()  # calling the training_validation function
#
#             trainModelObj = trainModel()  # object initialization
#             trainModelObj.trainingModel()  # training the model for the files in the table
#
#
#     except ValueError:
#
#         return Response("Error Occurred! %s" % ValueError)
#
#     except KeyError:
#
#         return Response("Error Occurred! %s" % KeyError)
#
#     except Exception as e:
#
#         return Response("Error Occurred! %s" % e)
#     return Response("Training successful!!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
