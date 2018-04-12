import os
import numpy as np
import pandas as pd
import shutil

IMAGES_ROOT_FOLDER = '/home/ramon/workspace/fast_and_curious/data/speedcam'
CLASSIFICATION_ROOT_FOLDER = '/home/ramon/workspace/fast_and_curious/classification'
KERAS_DATA_FOLDER = '/home/ramon/workspace/fast_and_curious/data'


def create_list_all_files():
        files_list  = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(IMAGES_ROOT_FOLDER)] for val in sublist]
        files_list = [(f,f.split('/')[-1]) for f in files_list]
        df_all_images_files = pd.DataFrame(files_list)
        df_all_images_files.to_csv('df_all_images_files.csv')
        df_all_images_files.columns = ['path','filename']
        return df_all_images_files

def filter_images_on_checked_images(df):
    df_checked_images = pd.read_csv('df_classified_and_checked.csv')
    df = pd.merge(df_checked_images,df, left_on='filename',right_on='filename',how='inner')
    import ipdb; ipdb.set_trace()
    return df


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)



def create_category_folders(df):
    create_folder(os.path.join(KERAS_DATA_FOLDER,'train'))
    create_folder(os.path.join(KERAS_DATA_FOLDER,'validation'))

    categories = df.category.unique().tolist()
    for c in categories:
        create_folder(os.path.join(KERAS_DATA_FOLDER,'train',c))
        create_folder(os.path.join(KERAS_DATA_FOLDER,'validation',c))


def copy_images_files_in_keras_data_folder(df):
    msk = np.random.rand(len(df)) < 0.8
    train = df[msk]
    validation =  df[~msk]
   
    for index, row in train.iterrows():
        if os.stat(row['path']).st_size != 0:
            shutil.copy2(row['path'],os.path.join(KERAS_DATA_FOLDER,'train',row['category']) )

    for index, row in validation.iterrows():
        if os.stat(row['path']).st_size != 0:
            shutil.copy2(row['path'],os.path.join(KERAS_DATA_FOLDER,'validation',row['category']) )


if __name__ == '__main__':
    df_all_images_files = create_list_all_files()
    df_all_images_files = filter_images_on_checked_images(df_all_images_files)
    df_classif = pd.read_csv('df_classif.csv')
    df_classif =df_classif.drop('path', 1)
    df = pd.merge(df_all_images_files,df_classif,on='filename')
    #df = df[df.category!='undefined']
    print(df.category.value_counts())
    df.category = df.category.str.replace('taxi', 'auto')
    df.category = df.category.str.replace('delivery', 'auto')
    df.category = df.category.str.replace('truck', 'auto')
    df.category = df.category.str.replace('ambulance', 'auto')
    df.category = df.category.str.replace('bus', 'auto')
    df.category = df.category.str.replace('moto', 'auto')
    df.category = df.category.str.replace('foot', 'bike')
    print(df.category.value_counts())
    df = df[df.category.str.contains('|'.join(['auto','bike']))]
    number_samples = df.category.value_counts().min()
    df = df.groupby('category').apply(lambda x: x.sample(number_samples))
    df.reset_index(drop=True)
    #import ipdb; ipdb.set_trace()
    create_category_folders(df)
    copy_images_files_in_keras_data_folder(df)
    
    
    