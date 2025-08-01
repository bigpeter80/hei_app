# Generated by Django 5.2.4 on 2025-07-30 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('huespedes', '0001_initial'),
        ('reservas', '0005_reserva_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='cantidad_adultos',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='reserva',
            name='cantidad_ninios',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ReservaHuesped',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('adulto', 'Adulto'), ('nino', 'Niño')], max_length=10)),
                ('huesped', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='huespedes.huesped')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='huespedes_reserva', to='reservas.reserva')),
            ],
        ),
        migrations.AddField(
            model_name='reserva',
            name='huespedes',
            field=models.ManyToManyField(blank=True, related_name='reservas', through='reservas.ReservaHuesped', to='huespedes.huesped'),
        ),
    ]
