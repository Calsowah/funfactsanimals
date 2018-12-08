from keras import applications 
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.applications.vgg16 import preprocess_input, VGG16, decode_predictions
import numpy as np

###### TODO make this not jank : - )
BEAR_TEST_SAMPLES = 110
FLAMINGO_TEST_SAMPLES = 110
IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 10

datagen = ImageDataGenerator(rescale=1./255)
model = applications.VGG16(include_top=False, weights='imagenet')
test_gen = datagen.flow_from_directory(
    'images/test',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode=None,
    shuffle=False
)
bottleneck_features_test = model.predict_generator(test_gen,
                            (BEAR_TEST_SAMPLES+FLAMINGO_TEST_SAMPLES) // BATCH_SIZE)
np.save(open('bottleneck/bottleneck_features_test.npy', 'wb'), 
        bottleneck_features_test)

test_data = np.load(open('bottleneck/bottleneck_features_test.npy', 'rb'))
model = load_model('models/flamingobear.h5')
preds = model.predict(test_data, batch_size=BATCH_SIZE).astype(int).flatten()

y = np.array( 
    [0] * BEAR_TEST_SAMPLES + 
    [1] * FLAMINGO_TEST_SAMPLES
)

# sketchy tester thing
print(float((preds != y).sum()) / preds.size)