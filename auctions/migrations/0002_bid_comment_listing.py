# Generated by Django 3.1.1 on 2020-09-20 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('category', models.IntegerField(choices=[(0, ''), (1, 'Fashion'), (2, 'Toys'), (3, 'Electronics'), (4, 'Home')], default=0)),
                ('post_time', models.DateField(auto_now_add=True)),
                ('close_time', models.DateField()),
                ('starting_bid', models.DecimalField(decimal_places=2, max_digits=9)),
                ('closed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_time', models.DateField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='auctions.listing')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='auctions.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_time', models.DateField(auto_now_add=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('success', models.BooleanField(default=False)),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bids', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]