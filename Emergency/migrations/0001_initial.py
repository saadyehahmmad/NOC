# Generated by Django 5.0.3 on 2024-03-30 20:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Emergency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('note', models.TextField(default='Nothing')),
                ('timestamp', models.DateTimeField(null=True)),
                ('distance', models.FloatField(null=True)),
                ('nurse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nurse_emergencys', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_emergencys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('note', models.TextField(default='Nothing')),
                ('is_active', models.BooleanField(default=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('distance', models.FloatField(null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_emergency_requests', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_emergency_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
