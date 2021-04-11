import dlib
import os
import numpy as np
from skimage import io
from scipy.spatial import distance
import shutil
from os import listdir
from os.path import isfile, join
import threading
from background_task import background
from asgiref.sync import sync_to_async


dirpath='../media/image_base'
resultpath='find_photos_1/'
obrazec='find.jpeg'
vsego=0


def getfilelist(dirpath):
    global vsego
    mas=[]
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            fullname = os.path.join(root, name)
            if('.jpg' in fullname or '.JPEG' in fullname or '.JPG' in fullname or '.jpeg' in fullname):
                mas.append(fullname)
    vsego=str(len(mas))
    print('Готовится к анализу: '+vsego+' фотографий')
    return mas


# Получаем цифровое представление найденных на фото лиц
# Функция возвращает массив с биометрией лиц
def get_face_descriptors(filename, sp, face_rec, detector):
    facemas=[]
    img = io.imread(filename)
    detected_faces = detector(img, 1)
    shape = None
    face_descriptor = None
    for k, d in enumerate(detected_faces):
        shape = sp(img, d)
        try:
            face_descriptor = face_rec.compute_face_descriptor(img, shape)
            if(face_descriptor!=None):
                facemas.append(face_descriptor)
        except Exception as ex:
            pass
    return facemas


def find_photos_1(image):
    print('START')
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    face_rec = dlib.face_recognition_model_v1(
        'dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    min_distance = 2

    f1 = get_face_descriptors(image, sp, face_rec, detector)[0]
    files = getfilelist(dirpath)
    flag = 0
    for f in files:
        flag = flag + 1
        print('Анализ ' + f + ' - ' + str(flag) + ' фото из ' + str(vsego))
        if os.path.exists(f):
            try:
                findfaces = get_face_descriptors(f)
                print('На фото: ' + str(len(findfaces)) + ' лиц')
                for f2 in findfaces:
                    if (f2 != []):
                        euc_distance = distance.euclidean(f1, f2)
                        print(euc_distance)
                        if euc_distance < 0.65:
                            print('Найдено лицо: ' + f)
                            shutil.copyfile(f, resultpath + str(flag) + '.jpg')
            except:
                continue
    print("DONE")
