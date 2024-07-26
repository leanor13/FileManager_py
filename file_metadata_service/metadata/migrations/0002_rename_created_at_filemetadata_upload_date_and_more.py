# Generated by Django 5.0.7 on 2024-07-26 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("metadata", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="filemetadata",
            old_name="created_at",
            new_name="upload_date",
        ),
        migrations.AlterField(
            model_name="filemetadata",
            name="file_size",
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name="filemetadata",
            name="file_url",
            field=models.CharField(max_length=1024),
        ),
        migrations.AddIndex(
            model_name="filemetadata",
            index=models.Index(
                fields=["file_size"], name="metadata_fi_file_si_f68e78_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="filemetadata",
            index=models.Index(
                fields=["file_type"], name="metadata_fi_file_ty_a21719_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="filemetadata",
            index=models.Index(
                fields=["file_name"], name="metadata_fi_file_na_4a686c_idx"
            ),
        ),
    ]