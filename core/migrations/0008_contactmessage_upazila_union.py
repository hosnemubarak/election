# Generated migration for adding upazila and union fields to ContactMessage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_event_options_alter_pressrelease_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='upazila',
            field=models.CharField(choices=[('lohagara', 'লোহাগাড়া'), ('satkania', 'সাতকানিয়া')], default='lohagara', max_length=50, verbose_name='উপজেলা'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='union',
            field=models.CharField(choices=[('lohagara_union', 'লোহাগাড়া ইউনিয়ন'), ('padua', 'পদুয়া'), ('barahatia', 'বড়হাতিয়া'), ('amirabad', 'আমিরাবাদ'), ('adhunagar', 'আধুনগর'), ('chunati', 'চুনতি'), ('charamba', 'চরাম্বা'), ('putibila', 'পুটিবিলা'), ('kalauzan', 'কালাউজান'), ('satkania_pourashava', 'সাতকানিয়া পৌরসভা'), ('satkania_union', 'সাতকানিয়া ইউনিয়ন'), ('dhemsha', 'ঢেমশা'), ('bazalia', 'বাজালিয়া'), ('kanchana', 'কাঞ্চনা'), ('keochia', 'কেঁওচিয়া'), ('madarsha', 'মাদার্শা'), ('purba_guchchagram', 'পূর্ব গুচ্ছগ্রাম')], default='lohagara_union', max_length=50, verbose_name='ইউনিয়ন/পৌরসভা'),
            preserve_default=False,
        ),
    ]
