# Generated by Django 5.0.2 on 2024-02-13 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0002_alter_review_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="body",
            field=models.CharField(
                blank=True, max_length=8192, verbose_name="comments"
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="headline",
            field=models.CharField(max_length=128, verbose_name="title"),
        ),
    ]
