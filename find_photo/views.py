import time
from django.shortcuts import render
from django.views import View
from .models import *
import dlib
import os
import numpy as np
from skimage import io
from scipy.spatial import distance
import shutil
from os import listdir
from os.path import isfile, join
import threading
# Create your views here.

dirpath='media/image_base'
resultpath='/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/find_photos/'
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


# @background(schedule=5)
def find_photos(image, group):
    sp = dlib.shape_predictor("/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/shape_predictor_68_face_landmarks.dat")
    face_rec = dlib.face_recognition_model_v1('/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    min_distance = 2

    f1 = get_face_descriptors(image, sp, face_rec, detector)[0]
    files = getfilelist(dirpath)
    flag = 0
    for f in files:
        flag = flag + 1
        print('Анализ ' + f + ' - ' + str(flag) + ' фото из ' + str(vsego))
        if os.path.exists(f):
            # try:
                findfaces = get_face_descriptors(f, sp, face_rec, detector)
                print('На фото: ' + str(len(findfaces)) + ' лиц')
                for f2 in findfaces:
                    if (f2 != []):
                        euc_distance = distance.euclidean(f1, f2)
                        print(euc_distance)
                        if euc_distance < 0.65:
                            print('Найдено лицо: ' + f)
                            shutil.copyfile(f, resultpath + str(flag) + '.jpg')
            # except:
            #     print("Exception", )
            #     continue
    print("DONE")
    onlyfiles = [f for f in listdir('/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/find_photos') if isfile(join('/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/find_photos', f))]

    for f in onlyfiles:
        image = Images.objects.create(image=f'/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/find_photos/{f}')
        group.find_images.add(image)
    group.save()


class Main(View):
    def post(self, request):
        images = Images.objects.all()

        image = request.FILES.get('image')
        name = request.POST.get('name')

        if not image and not name:
            # images = Images.objects.all()
            return render(request, 'find_photo/main.html', context={'images': images, 'result': True, })
        group = Groups.objects.create(photo=image, title=name,)
        find_photos("/home/azamat/PycharmProjects/Exam_Machine_learning/" + group.photo.url, group)
        print(group.photo)
        # x = threading.Thread(target=find_photos, args=("/home/azamat/PycharmProjects/Exam_Machine_learning/" + group.photo.url,))
        # x.setDaemon(True)
        # x.start()
        #
        # print(x.is_alive())

        # mypath = '/find_photos/'
        # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        #
        # for file in onlyfiles:
        #     print(file)
        #     group.find_images.add(file)
        # group.save()
        return render(request, 'find_photo/main.html', context={'images': images, })

        # return render(request, 'find_photo/group_detail.html', context={'group': group})

    def get(self, request):
        images = Images.objects.all()
        groups = Groups.objects.all()

        return render(request, 'find_photo/main.html', context={'images': images, })


class GroupDetail(View):
    def get(self, request, id):
        group = Groups.objects.get(id=id)

        return render(request, 'find_photo/group_detail.html', context={'group': group, })
