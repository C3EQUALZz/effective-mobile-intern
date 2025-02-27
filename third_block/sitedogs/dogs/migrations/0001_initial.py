# Generated by Django 5.1.5 on 2025-01-24 19:38

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Breed",
            fields=[
                ("oid", models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "size",
                    models.CharField(
                        choices=[("Tiny", "Tiny"), ("Small", "Small"), ("Medium", "Medium"), ("Large", "Large")],
                        max_length=10,
                    ),
                ),
                (
                    "friendliness",
                    models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
                ),
                (
                    "train_ability",
                    models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
                ),
                (
                    "shedding_amount",
                    models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
                ),
                (
                    "exercise_needs",
                    models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dog",
            fields=[
                ("oid", models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("age", models.PositiveIntegerField()),
                ("gender", models.CharField(choices=[("Male", "Male"), ("Female", "Female")], max_length=10)),
                ("color", models.CharField(max_length=50)),
                ("favorite_food", models.CharField(blank=True, max_length=255, null=True)),
                ("favorite_toy", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "breed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="dogs", to="dogs.breed"
                    ),
                ),
            ],
        ),
    ]
