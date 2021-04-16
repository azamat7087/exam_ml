# Generated by Django 3.1.1 on 2021-04-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_photo', '0006_auto_20210411_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image_base')),
                ('index', models.IntegerField(blank=True, editable=False, null=True)),
                ('date_of_add', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Gallery',
                'ordering': ['index'],
            },
        ),
        migrations.AlterModelOptions(
            name='images',
            options={'verbose_name_plural': 'Images'},
        ),
        migrations.RemoveField(
            model_name='images',
            name='index',
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to='find_images'),
        ),
    ]