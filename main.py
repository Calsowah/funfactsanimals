from keras import applications
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from imagekitio.client import Imagekit
from six.moves import urllib
from funFactScraper import getFunFacts
from PIL import Image
import numpy as np
import os
import base64
import re
import sys
import requests
import json

### CONSTANTS
IMG_WIDTH, IMG_HEIGHT = 224, 224      # size that input image will be resized to
# all possible animals (alphabetical order)
ANIMALS = ['bear', 'flamingo', 'fox', 'giraffe', 'red winged blackbird', 'zebra']
BATCH_SIZE = 1

### IMAGEKIT STUFF
apiKey = "Yt05Bmz0RCGbvb69lJ9IEbkhtcA="  # required
apiSecret = "HQcl+rw5UEbX68vQu4ffZo3mQwE="  # required and to be kept secret
imagekitId = "hjq03h7yv"  # required

client = Imagekit({"api_key": apiKey,
                   "api_secret": apiSecret,
                   "imagekit_id": imagekitId,
                   "use_subdomain": False,
                   "use_secure": True})


### Initialize models
vgg16_model = applications.VGG16(include_top=False, weights='imagenet')
model = load_model('models/model_adam.h5') # TODO change this to our final trained model

def classify(img):
    """ Classify a single input image.
        Prints the classification output and a fun fact to the console.
    
        img: relative path to a jpg image to classify [string]
        returns: the predicted animal name [string], fun fact about the animal
    """
    # possible TODO: call the imagekit script on the input image
    img = load_img(img, target_size=(IMG_WIDTH, IMG_HEIGHT))
    np_img = img_to_array(img) # (224, 224, 3)
    np_img = np_img.reshape((1,) + np_img.shape) # (1, 224, 224, 3)
    datagen = ImageDataGenerator(rescale=1./255).flow(
                np_img, 
                batch_size=BATCH_SIZE
    )
        
    # make prediction
    # predict_classes will return the label, which is an integer (0, 1, 2... for
    # each animal in alphabetical order)
    # convert this to a string name, then return
    bottleneck_features_web = vgg16_model.predict_generator(datagen, BATCH_SIZE)
    prediction = model.predict_classes(bottleneck_features_web, batch_size=BATCH_SIZE)[0]
    animal = ANIMALS[prediction]
    fun_fact = getFunFacts(animal)
    # article = "an " if fun_fact[0].lower() in ['a','e','i','o','u'] else "a "
    # text = "This is " + article + animal + "!\nDid you know? \n" + fun_fact + "\n\n"
    # print(text) # idk if we want to remove this

    return json.dumps({'result': prediction, 'fun': fun_fact})

if __name__ == '__main__':
    classify('DEMOIMAGES/flamingo.jpg')
    classify('DEMOIMAGES/fox.jpg')
    classify('DEMOIMAGES/giraffe.jpg')
    classify('DEMOIMAGES/rwblackbird.jpg')
    classify('DEMOIMAGES/zebra.jpg')


