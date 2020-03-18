# Generated by Django 3.0.4 on 2020-03-16 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('patronymic', models.CharField(blank=True, max_length=50)),
                ('pseudonym', models.CharField(max_length=50, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('birthday', models.DateField()),
                ('deathday', models.DateField(blank=True, null=True)),
                ('country', models.CharField(max_length=50)),
                ('biography', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='')),
                ('year_made', models.PositiveSmallIntegerField()),
                ('page_count', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublisherCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Publisher companies',
            },
        ),
        migrations.CreateModel(
            name='BookAuthorsPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveSmallIntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.Author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.Book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='books', through='library_app.BookAuthorsPriority', to='library_app.Author'),
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(related_name='books', to='library_app.Genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library_app.PublisherCompany'),
        ),
        migrations.AddField(
            model_name='author',
            name='genres',
            field=models.ManyToManyField(related_name='authors', to='library_app.Genre'),
        ),
    ]
