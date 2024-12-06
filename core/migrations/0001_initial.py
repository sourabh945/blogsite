# Generated by Django 5.1 on 2024-12-05 14:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(error_messages={'unqiue': 'Author with this email address already exists'}, max_length=126, unique=True, verbose_name='author email address')),
                ('username', models.CharField(error_messages={'unique': 'Author with this username already exists'}, max_length=126, primary_key=True, serialize=False, unique=True, verbose_name='username of the author')),
                ('name', models.CharField(blank=True, max_length=126, null=True, verbose_name='name of user')),
                ('tags', models.JSONField(blank=True, default=list, verbose_name='tags for blog that user like')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id of the blog')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('date_of_pub', models.DateTimeField(auto_now_add=True, verbose_name='date of publication')),
                ('content', models.TextField(max_length=5000, verbose_name='content of the blog')),
                ('tags', models.JSONField(blank=True, verbose_name='tags')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='author username')),
            ],
        ),
    ]
