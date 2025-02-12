# Generated by Django 5.1.6 on 2025-02-10 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(help_text='Email или номер телефона', max_length=255, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id_type',
            field=models.CharField(choices=[('email', 'Email'), ('phone', 'Телефон')], editable=False, help_text='Тип идентификатора', max_length=10),
        ),
    ]
