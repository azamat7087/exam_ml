import time
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
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
resultpath='/home/azamat/PycharmProjects/Exam_Machine_learning/media/find_images/'
obrazec='find.jpeg'
vsego=0


def get_id():
    id = str(random.randint(1, 9999999999999999))
    return id


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
def find_photos(image, group, request):
    start = time.time()
    sp = dlib.shape_predictor("/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/shape_predictor_68_face_landmarks.dat")
    face_rec = dlib.face_recognition_model_v1('/home/azamat/PycharmProjects/Exam_Machine_learning/find_photo/dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()
    min_distance = 2
    name = group.title.replace(" ", '_')
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
                            i = get_id()
                            shutil.copyfile(f, resultpath + str(name) + str(i) + '.jpg')
            # except:
            #     print("Exception", )
            #     continue
    print("DONE")
    onlyfiles = [f for f in listdir('/home/azamat/PycharmProjects/Exam_Machine_learning/media/find_images') if isfile(join('/home/azamat/PycharmProjects/Exam_Machine_learning/media/find_images', f))]

    for f in onlyfiles:
        if f.__contains__(name):
            image = Images.objects.create()
            image.image = f
            image.save()
            print(image.id, image.image)
            group.find_images.add(image)
            group.is_ready = True
    group.save()
    print(time.time() - start)


class Main(View):
    def post(self, request):
        images = Images.objects.all()
        groups = Groups.objects.all()
        image = request.FILES.get('image')
        name = request.POST.get('name')

        if not image and not name:
            return render(request, 'find_photo/main.html', context={'images': images, 'result': 'Введите название и фотографию', })
        try:
            group = Groups.objects.create(photo=image, title=name,)
        except IntegrityError:
            return render(request, 'find_photo/main.html', context={'images': images, 'result': 'Группа с таким названием уже существует', })
        # find_photos("/home/azamat/PycharmProjects/Exam_Machine_learning/" + group.photo.url, group, request)
        x = threading.Thread(target=find_photos, args=("/home/azamat/PycharmProjects/Exam_Machine_learning/" + group.photo.url, group, request))
        x.setDaemon(True)
        x.start()

        return render(request, 'find_photo/please_wait.html', context={'images': images, 'groups': groups, })

    def get(self, request):
        images = Gallery.objects.all()
        groups = Groups.objects.all()

        return render(request, 'find_photo/main.html', context={'images': images, 'groups': groups, })


class GroupDetail(View):
    def get(self, request, id):
        group = Groups.objects.get(id=id)

        return render(request, 'find_photo/group_detail.html', context={'group': group, })
