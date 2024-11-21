# news/management/commands/save_data.py
from django.core.management.base import BaseCommand
from django.apps import apps
import json
import csv
from django.db import models

class Command(BaseCommand):
    help = 'Saves data from a specified Django model to a JSON or CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='The name of the model to save data from (e.g., app_label.ModelName)')
        parser.add_argument('file_path', type=str, help='Path to save the JSON or CSV file')
        parser.add_argument('--format', type=str, choices=['json', 'csv'], required=True, help='Format of the data file (json or csv)')

    def handle(self, *args, **options):
        model_name = options['model']
        file_path = options['file_path']
        data_format = options['format']

        # Load the model
        try:
            model = apps.get_model(model_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(f'Model "{model_name}" not found'))
            return

        # Query all data from the model
        queryset = model.objects.all()
        
        # Process the file based on the format
        if data_format == 'json':
            self.save_json(queryset, file_path)
        elif data_format == 'csv':
            self.save_csv(queryset, file_path)

    def save_json(self, queryset, file_path):
        data = [self.serialize_instance(instance) for instance in queryset]

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Successfully saved data from queryset to {file_path} as JSON'))

    def save_csv(self, queryset, file_path):
        data = [self.serialize_instance(instance) for instance in queryset]

        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f'Successfully saved data from queryset to {file_path} as CSV'))

    def serialize_instance(self, instance):
        """Converts a model instance to a dictionary, converting foreign keys to <field_name>_id."""
        data = {}
        for field in instance._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                # Convert foreign key to <field_name>_id
                related_instance = getattr(instance, field.name)
                data[f"{field.name}_id"] = related_instance.pk if related_instance else None
            elif isinstance(field, models.ManyToManyField):
                # For many-to-many fields, store a list of IDs to allow for serialization
                data[field.name] = list(getattr(instance, field.name).values_list('id', flat=True))
            else:
                data[field.name] = getattr(instance, field.name)
        return data
