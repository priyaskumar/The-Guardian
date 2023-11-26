# Generated by Django 4.2.6 on 2023-11-25 17:59

from django.db import migrations, models
# Generated by Django 4.2.6 on 2023-11-26 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.TextField()),
                ('time', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('specialization', models.CharField(max_length=255)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=255)),
                ('type_of_disease', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('doa', models.DateField()),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('last_checkup', models.DateField(blank=True, null=True)),
                ('threshold_heart_rate', models.IntegerField(blank=True, null=True)),
                ('threshold_bp_rate', models.IntegerField(blank=True, null=True)),
                ('threshold_spo2_rate', models.IntegerField(blank=True, null=True)),
                ('threshold_co2_rate', models.IntegerField(blank=True, null=True)),
                ('doctors', models.ManyToManyField(to='theGuardian.doctor')),
            ],
        ),
    ]
