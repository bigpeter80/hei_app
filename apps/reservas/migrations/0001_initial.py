# Generated by Django 5.2.4 on 2025-07-28 11:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0003_alter_cliente_dni_alter_cliente_email'),
        ('habitaciones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateField()),
                ('fecha_salida', models.DateField()),
                ('deposito', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('informacion_adicional', models.TextField(blank=True, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('modificado_en', models.DateTimeField(auto_now=True)),
                ('eliminado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.cliente')),
                ('creado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservas_creadas', to=settings.AUTH_USER_MODEL)),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='habitaciones.habitacion')),
                ('modificado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservas_modificadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
