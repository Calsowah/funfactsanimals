from keras import applications
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from imagekitio.client import Imagekit
from six.moves import urllib
import os
import base64
import re
import sys
from PIL import Image
import requests

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
    
        img: relative path to a jpg image to classify [string]
        returns: the predicted animal name [string]
    """
    # possible TODO: call the imagekit script on the input image
    '''img = load_img(img, target_size=(IMG_WIDTH, IMG_HEIGHT))
    np_img = img_to_array(img) # (224, 224, 3)
    np_img = np_img.reshape((1,) + np_img.shape) # (1, 224, 224, 3)
    datagen = ImageDataGenerator(rescale=1./255).flow(
                np_img, 
                batch_size=BATCH_SIZE
    )'''

    with open(img, "rb") as image_file:
        img = base64.b64encode(image_file.read())
        obj = {
            "filename": "test_img.jpg",
            "folder": "/"
        }
        # upload to imagekitio
        response = client.upload(img, obj)
    
        # get thumbnail url from imagekitio and add transformation
        url_thumb = (re.sub('/tr:n-media_library_thumbnail/', '/tr:h-224,w-224,fo-auto/', str(response.get("thumbnail"))))
        response = requests.get(url_thumb)
        np_img = np.array(Image.open(StringIO(response.content))) # (224, 224, 3)
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
    return ANIMALS[prediction]
