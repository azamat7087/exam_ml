from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.


class Main(View):
    def post(self, request):

        return render(request, 'find_photo/main.html', context={ })

    def get(self, request):
        images = Images.objects.all()
        groups = Groups.objects.all()

        return render(request, 'find_photo/main.html', context={'images': images, })


class GroupDetail(View):
    def get(self, request, id):
        group = Groups.objects.get(id=id)

        return render(request, 'find_photo/group_detail.html', context={'group': group, })
