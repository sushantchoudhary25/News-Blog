# Generated by Django 3.1.1 on 2020-09-12 13:32

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(default='test'),
            preserve_default=False,
        ),
    ]