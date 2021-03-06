from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from controller.wafer_finder import WaferFinder
from controller.wafer_predictor import WaferPredictor
from controller.wafer_pattern_manager import WaferPatternManager
import os
import pickle

app = Flask(__name__)
api = Api(app)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_DIR,"frontend")
DATA_DIR = os.path.join(ROOT_DIR,"../../data")
TRAINING_DATA_DIR = os.path.join(DATA_DIR,"training_maps")
BACKEND_DIR = os.path.join(ROOT_DIR, "../backend")
model_pickle_file = os.path.join(BACKEND_DIR,"model.p")
model = pickle.load(open(model_pickle_file,"rb"))


@app.route('/app/<path:path>')
def serve_page(path):
    # print("Serving file : ",APP_DIR,"/" ,path)
    return send_from_directory( APP_DIR, path)


api.add_resource(WaferFinder, '/map/<string:wafer_id>', endpoint='map', resource_class_kwargs={ 'data_dir': TRAINING_DATA_DIR })
api.add_resource(WaferFinder, '/map', endpoint='maplist', resource_class_kwargs={ 'data_dir': TRAINING_DATA_DIR })
api.add_resource(WaferPredictor, '/wafer_predictor', endpoint='wafer_predictor', resource_class_kwargs={ 'model': model })
api.add_resource(WaferPatternManager, '/wafer_pattern_manager', endpoint='wafer_pattern_generator', resource_class_kwargs={ 'data_dir': DATA_DIR })


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0' port=8080, debug=True)
