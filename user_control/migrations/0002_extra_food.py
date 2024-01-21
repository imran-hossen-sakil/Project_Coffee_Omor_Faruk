# Generated by Django 4.2.2 on 2024-01-14 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra_Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('detaild', models.TextField()),
                ('amount', models.FloatField()),
                ('c_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_control.consumer_user')),
                ('entry_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
