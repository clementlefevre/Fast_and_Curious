from os import listdir
from os.path import isfile,join
from os import walk
import cv2
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.callbacks import ReduceLROnPlateau
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras import metrics
import pandas as pd
from flask.settings import GALLERY_ROOT_DIR

from classifier_from_speedcam_script import create_model


nb_category = 1
# dimensions of our images.
img_width, img_height = 250, 250


def load_keras_model():
    model = create_model()

    model.load_weights('first_try.h5')

    model.compile(loss='binary_crossentropy',
                optimizer='rmsprop',
                metrics=['accuracy'])

    return model


def load_images_data():
    
    df_speedcam = pd.read_csv('speed-cam.csv',header=None)
    df_speedcam.columns = ["date","hour","minute","speed","Unit","Speed_Photo_Path",
      "X","Y","W","H","Area","Direction"]
    df_speedcam['filename'] = df_speedcam.Speed_Photo_Path.apply(lambda x: x.split('/')[-1])
    return df_speedcam
    

def load_images_paths():
   
    files_list  = [val for sublist in [[join(i[0], j) for j in i[2]] for i in walk(GALLERY_ROOT_DIR)] for val in sublist]
    print ('Number of Pictures in image folder :{}'.format(len(files_list)))
    files_list = [f for f in files_list if '.jpg' in f]
    df_files_paths = pd.DataFrame(files_list)
    df_files_paths.columns = ['file_path']
    df_files_paths['filename'] = df_files_paths.file_path.apply(lambda x: x.split('/')[-1])
    return df_files_paths



def predict(filename,model):

    img = cv2.imread(filename)
    img = cv2.resize(img,(250,250))
    img = np.reshape(img,[1,250,250,3])
    img = img /255.0

    classes = model.predict_classes(img)
   
    return classes[0][0]
    

files = [''.join(['data/test/',f]) for f in listdir('data/test/') if isfile(join('data/test/', f))]

if __name__=='__main__':
    df_images_data = load_images_data()
    df_images_paths = load_images_paths()
    df = pd.merge(df_images_paths,df_images_data,on='filename', how='inner')
    model = load_keras_model()
    df['classes']= df.file_path.apply(lambda x :predict(x,model))
    df.to_csv('df_after_prediction.csv')
    