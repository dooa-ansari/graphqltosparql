# Generated by Django 4.2.7 on 2025-01-28 15:43

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
            name='PropertyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('datatype', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distinct', models.BooleanField(default=False)),
                ('ordered', models.BooleanField(default=False)),
                ('bindings', models.ManyToManyField(related_name='results', to='sparql_main.binding')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sparql_main.head')),
                ('results', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sparql_main.results')),
            ],
        ),
        migrations.AddField(
            model_name='binding',
            name='accessURL',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accessURL_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='description',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='description_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='distribution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='distribution_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='geometry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='geometry_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='identifier',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='identifier_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='license',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='license_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='maintainerEmail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='maintainerEmail_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='mediaType',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mediaType_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='modified',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='modified_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='publisherName',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='publisherName_binding', to='sparql_main.propertytype'),
        ),
        migrations.AddField(
            model_name='binding',
            name='title',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='title_binding', to='sparql_main.propertytype'),
        ),
    ]
