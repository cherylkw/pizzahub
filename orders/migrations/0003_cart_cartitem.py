# Generated by Django 2.2.10 on 2020-03-26 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_auto_20200326_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_id', models.IntegerField()),
                ('size_type', models.CharField(default='N', max_length=1)),
                ('cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitem_cat', to='orders.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Create', max_length=64)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('item', models.ManyToManyField(to='orders.CartItem')),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userorder_id', to='orders.UserOrder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
