from django.db import models
import random

# Create your models here.


def get_index(index):
    indexes = UsedIndexes.objects.all()
    indexes_arr = []
    for index1 in indexes:
        indexes_arr.append(index1.index)
    while True:
        for i in range(0, 10):
            if i == index:
                index = random.randint(i * 10000, (i + 1) * 10000 - 1)
                break
        if index not in indexes_arr:
            UsedIndexes.objects.create(index=index)
            return index


class UsedIndexes(models.Model):
    index = models.PositiveIntegerField()

    def __str__(self):
        return str(self.index)


class Images(models.Model):
    image = models.ImageField(upload_to='find_images', null=True, blank=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            i = random.randint(0, 10)
            self.index = get_index(i)

        super(Images, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Images'


class Gallery(models.Model):
    image = models.ImageField(upload_to='image_base')
    index = models.IntegerField(blank=True, null=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            i = random.randint(0, 10)
            self.index = get_index(i)

        super(Gallery, self).save(*args, **kwargs)

    class Meta:
        ordering = ['index']
        verbose_name_plural = 'Gallery'


class Groups(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_ready = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="find_photos")
    find_images = models.ManyToManyField(Images, related_name="group", blank=True, )
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Groups'
