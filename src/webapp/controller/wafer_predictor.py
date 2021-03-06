from flask_restful import Resource
from flask import url_for, request
import numpy as np



class WaferPredictor(Resource) :

    def __init__(self, **kwargs):
        self.model = kwargs["model"]

    def post(self):
        json_data = request.get_json(force=True)
        coord = [k.split(",") for k in json_data["mapData"].keys()]
        mapLineArray = self.coordToMap(coord)
        # print(mapLineArray)
        X = np.array(mapLineArray)
        X = X.reshape(1, -1)
        result = self.model.predict(X)
        print(coord)
        print(result)

        proba = self.model.predict_proba(X)
        class_to_proba= {}
        for i,c in enumerate(self.model.classes_) :
            class_to_proba[c] = proba[0][i]
        print(class_to_proba)
        print(proba)
        resp = {
            "pattern" : result[0],
            "class_to_proba" : class_to_proba
        }

        return resp, 200


    def coordToMap(self, arrayOfCoord):
        rows = 100;
        cols = 100;
        map = [0] * (rows * cols)
        for xy in arrayOfCoord :
            x = int(xy[0])
            y = int(xy[1])
            # print(x, ",", y)
            idx = (y * cols) + x
            map[idx] = 1
        return map