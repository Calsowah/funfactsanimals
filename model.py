from keras import applications 
from keras import optimizers 
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D
from os import path
import numpy as np
import argparse

### CONSTANTS ###
TRAIN_SAMPLES = 4000 # total number of training samples across all classes
VAL_SAMPLES = 400    # total number of validation samples across all classes
NB_CLASSES = 2       # number of classes
EPOCHS = 50          # number of epochs
BATCH_SIZE = 16      # batch size - nb samples should be divisible by this
WIDTH, HEIGHT = 224, 224 # size to which the images will be resized - VGG16 expects 224x224

# paths to directories containing training/validation images, and bottleneck features
TRAIN_DIR = path.join('images','train') 
VAL_DIR   = path.join('images','validation')
TRAIN_BOTTLENECK = path.join('bottleneck', 'bottleneck_features_train.npy')
VAL_BOTTLENECK   = path.join('bottleneck', 'bottleneck_features_val.npy')

def load_vgg16():
    datagen = ImageDataGenerator(rescale=1./255)
    
    # build VGG16 network and save bottleneck features 
    # for training & validation sets
    model = applications.VGG16(include_top=False, weights='imagenet')
    train_gen = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(WIDTH, HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode=None,
        shuffle=False
    )

    bottleneck_features_train = model.predict_generator(train_gen,
                                TRAIN_SAMPLES // BATCH_SIZE)
    np.save(open(TRAIN_BOTTLENECK, 'wb'), bottleneck_features_train)

    validation_gen = datagen.flow_from_directory(
        VAL_DIR,
        target_size=(WIDTH, HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode=None,
        shuffle=False
    )
    
    bottleneck_features_val = model.predict_generator(validation_gen,
                              VAL_SAMPLES // BATCH_SIZE)
    np.save(open(VAL_BOTTLENECK, 'wb'), bottleneck_features_val)

def train(dest):
    # load bottleneck features
    train_data = np.load(open(TRAIN_BOTTLENECK, 'rb'))
    val_data = np.load(open(VAL_BOTTLENECK, 'rb'))

    # generate labels for training and testing set
    # this assumes that each class has an equal number of training/validation samples
    train_labels = np.array( 
        [0] * (int(TRAIN_SAMPLES / NB_CLASSES)) + 
        [1] * (int(TRAIN_SAMPLES / NB_CLASSES))
    )
    val_labels = np.array(
        [0] * (int(VAL_SAMPLES / NB_CLASSES)) +
        [1] * (int(VAL_SAMPLES / NB_CLASSES))
    )

    # build model on top and train
    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', 
                  metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=EPOCHS,
              batch_size=BATCH_SIZE,
              validation_data=(val_data, val_labels),
              shuffle=True)

    model.save(dest)

if __name__ == '__main__':
    # parse CL arguments for where to save model
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', type=str, required=True, 
                        help='path to an h5 file [where model will be saved]')
    dest = vars(parser.parse_args())['dest']

    load_vgg16()
    train(dest)


