# Generated by Django 3.1 on 2020-08-23 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Name')),
                ('shares', models.IntegerField(verbose_name='Shares')),
                ('price', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Price')),
                ('total', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Total')),
                ('stock', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='stocks.transaction')),
            ],
        ),
    ]
