from keras import applications 
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
from keras.utils.np_utils import to_categorical
import numpy as np

TEST_MODEL = 'models/threeclass_test.h5' # path to the model being tested
TEST_SAMPLES = 330 # total number of test samples across all classes
NB_CLASSES = 3     # total number of classes
IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 10

datagen = ImageDataGenerator(rescale=1./255)
vgg16_model = applications.VGG16(include_top=False, weights='imagenet')
test_gen = datagen.flow_from_directory(
    'images/test',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode=None,
    shuffle=False
)
bottleneck_features_test = vgg16_model.predict_generator(test_gen,
                            TEST_SAMPLES // BATCH_SIZE)
model = load_model(TEST_MODEL)
preds = model.predict(bottleneck_features_test, batch_size=BATCH_SIZE).astype(int)

# generate actual labels & convert to one-hot encoding
y = np.concatenate([[i] * int(TEST_SAMPLES / NB_CLASSES) 
                    for i in range(NB_CLASSES)])
y = to_categorical(y, num_classes=3)

# print the test error
print(float((preds != y).sum()) / preds.size)