# Generated by Django 5.2.1 on 2025-05-11 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rankings", "0004_evaluationcategory_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="brandevaluationscore",
            options={},
        ),
        migrations.AlterUniqueTogether(
            name="brandevaluationscore",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="brandevaluationscore",
            name="notes",
            field=models.TextField(blank=True, null=True, verbose_name="메모"),
        ),
    ]
