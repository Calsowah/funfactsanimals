from keras import applications 
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D
from keras.utils.np_utils import to_categorical
from keras import regularizers
from os import path
from keras.callbacks import TensorBoard
from time import time
import numpy as np
import argparse

### CONSTANTS ###
NB_CLASSES = 6       # number of classes
EPOCHS = 50          # number of epochs
BATCH_SIZE = 48      # batch size - nb samples should be divisible by this
WIDTH, HEIGHT = 224, 224 # size to which the images will be resized - VGG16 expects 224x224
TRAIN_SAMPLES = NB_CLASSES*2000 # total number of training samples across all classes
VAL_SAMPLES = NB_CLASSES*200    # total number of validation samples across all classes

# paths to directories containing training/validation images, and bottleneck features
MODEL_PATH = path.join('models', 'model_adam.h5')
TRAIN_DIR = path.join('images','train') 
VAL_DIR   = path.join('images','validation')
TRAIN_BOTTLENECK = path.join('bottleneck', 'bottleneck_features_train.npy')
VAL_BOTTLENECK   = path.join('bottleneck', 'bottleneck_features_val.npy')

def parse():
    """ Parse command line arguments given by the user.
        USAGE:
        python model.py --dest [path to destination h5 file]
                        --train [path to directory containing training images]
                        --val [path to directory containing testing images]
        Returns: a dictionary mapping the parameter names to the values.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', type=str, default=MODEL_PATH, 
                        help='path to an h5 file where model will be saved [default: ./models/model.h5]')
    parser.add_argument('--train', type=str, default=TRAIN_DIR, 
                        help='path to the directory containing training images [default: ./images/train')
    parser.add_argument('--val', type=str, default=VAL_DIR, 
                        help='path to directory containing validation images [default: ./images/validation')
    return vars(parser.parse_args())

def load_vgg16(train_dir, val_dir):
    datagen = ImageDataGenerator(rescale=1./255)
    
    # build VGG16 network and save bottleneck features 
    # for training & validation sets
    model = applications.VGG16(include_top=False, weights='imagenet')
    train_gen = datagen.flow_from_directory(
        train_dir,
        target_size=(WIDTH, HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode=None,
        shuffle=False
    )

    bottleneck_features_train = model.predict_generator(train_gen,
                                TRAIN_SAMPLES // BATCH_SIZE)
    np.save(open(TRAIN_BOTTLENECK, 'wb'), bottleneck_features_train)

    validation_gen = datagen.flow_from_directory(
        val_dir,
        target_size=(WIDTH, HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode=None,
        shuffle=False
    )
    
    bottleneck_features_val = model.predict_generator(validation_gen,
                              VAL_SAMPLES // BATCH_SIZE)
    np.save(open(VAL_BOTTLENECK, 'wb'), bottleneck_features_val)

def train(dest):
    # intialize tensorboard to track training progress
    tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

    # load bottleneck features
    train_data = np.load(open(TRAIN_BOTTLENECK, 'rb'))
    val_data = np.load(open(VAL_BOTTLENECK, 'rb'))

    # generate labels for training and testing set, and convert to one-hot encoding
    # this assumes that each class has an equal number of training/validation samples
    train_labels = np.concatenate([[i] * int(TRAIN_SAMPLES / NB_CLASSES) 
                                   for i in range(NB_CLASSES)])
    train_labels = to_categorical(train_labels, num_classes=NB_CLASSES)
    val_labels = np.concatenate([[i] * int(VAL_SAMPLES / NB_CLASSES) 
                                   for i in range(NB_CLASSES)])
    val_labels = to_categorical(val_labels, num_classes=NB_CLASSES)

    # build model on top and train
    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))#, activity_regularizer=regularizers.l2(0.001)))
    model.add(Dropout(0.50))
    model.add(Dense(NB_CLASSES, activation='softmax'))

    model.compile(optimizer='adam',#'rmsprop',
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=EPOCHS,
              batch_size=BATCH_SIZE,
              validation_data=(val_data, val_labels),
              shuffle=True,
              callbacks=[tensorboard])

    model.save(dest)

if __name__ == '__main__':
    args = parse()
    # load_vgg16(args['train'], args['val'])
    train(args['dest'])


