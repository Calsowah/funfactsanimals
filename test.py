from keras import applications 
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
from keras.utils.np_utils import to_categorical
import numpy as np

TEST_MODEL = 'models/sixclass.h5' # path to the model being tested
# bear, flamingo, fox, giraffe, birdofred, zebra
TEST_SAMPLES = [110, 110, 110, 40, 110, 110]
NB_CLASSES = len(TEST_SAMPLES)     # total number of classes
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
                            sum(TEST_SAMPLES) // BATCH_SIZE)
model = load_model(TEST_MODEL)
preds = model.predict(bottleneck_features_test, batch_size=BATCH_SIZE).astype(int)

# generate actual labels & convert to one-hot encoding
y = np.concatenate([[i] * TEST_SAMPLES[i] for i in range(NB_CLASSES)])
y = to_categorical(y, num_classes=NB_CLASSES)

# print the test error
print(float((preds != y).sum()) / sum(TEST_SAMPLES))