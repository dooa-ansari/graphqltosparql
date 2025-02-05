# Generated by Django 4.2.7 on 2025-01-12 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Binding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distribution', models.URLField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('mediaType', models.CharField(blank=True, max_length=255, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('identifier', models.CharField(blank=True, max_length=255, null=True)),
                ('accessURL', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('geometry', models.JSONField(blank=True, null=True)),
                ('license', models.URLField(blank=True, null=True)),
                ('publisherName', models.CharField(blank=True, max_length=255, null=True)),
                ('maintainerEmail', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Head',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vars', models.JSONField()),
                ('link', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distinct', models.BooleanField(default=False)),
                ('ordered', models.BooleanField(default=False)),
                ('bindings', models.ManyToManyField(to='sparql_main.binding')),
            ],
        ),
        migrations.CreateModel(
            name='JsonData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sparql_main.head')),
                ('results', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sparql_main.results')),
            ],
        ),
    ]
