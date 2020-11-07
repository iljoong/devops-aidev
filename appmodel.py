"""
appmodel.py
"""

import numpy as np
from keras.models import load_model
from keras.preprocessing import image

class FruitsModel:
    def __init__(self, modelpath, blobacct, blobkey):
        self.labels = "apple;avocado;banana;cherry;mango;orange;peach".split(';')
        self.modelpath = modelpath
        self.blobacct = blobacct
        self.blobkey = blobkey
        self.model = None

    def load(self):
        """load model"""
        if (self.model == None):
            self.model = load_model(self.modelpath)

    def get(self):
        if (self.model == None):
            self.model = load_model(self.modelpath)

        return self.model

    def update(self, modelpath):
        self.modelpath = modelpath
        self.model = load_model(self.modelpath)

        return self.model

    def score(self, filepath):

        self.load()

        img = image.load_img(filepath, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x /= 255.

        classes = self.model.predict(x)
        result = np.squeeze(classes)
        result_indices = np.argmax(result)

        return self.labels[result_indices], result[result_indices]*100
    
    def get_blob(self):
        return self.blobacct, self.blobkey

    def get_diag(self):
        return self.blobacct, self.blobkey, self.modelpath