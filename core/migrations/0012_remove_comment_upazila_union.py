# Generated manually to remove upazila and union fields from Comment model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_comment_union_comment_upazila'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='upazila',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='union',
        ),
    ]
