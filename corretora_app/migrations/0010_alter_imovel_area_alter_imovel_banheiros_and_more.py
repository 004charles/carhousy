# Generated by Django 5.1.6 on 2025-02-06 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corretora_app', '0009_imovel_apresentar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='area',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Área total do imóvel em metros quadrados', max_digits=6),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='banheiros',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='quartos',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='vagas_garagem',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
