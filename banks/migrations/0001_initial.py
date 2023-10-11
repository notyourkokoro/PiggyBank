# Generated by Django 4.2.5 on 2023-10-07 07:28

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
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, null=True)),
                ('goal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='banks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
