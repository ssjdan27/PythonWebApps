# news/management/commands/load_data.py
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
import json
import csv
import os

class Command(BaseCommand):
    help = 'Loads data from a JSON or CSV file into a specified Django model'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='The name of the model to load data into (e.g., app_label.ModelName)')
        parser.add_argument('file_path', type=str, help='Path to the JSON or CSV file')
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

        # Check file existence
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'File "{file_path}" not found'))
            return

        # Delete existing data
        model.objects.all().delete()

        # Process the file based on the format
        if data_format == 'json':
            self.load_json(model, file_path)
        elif data_format == 'csv':
            self.load_csv(model, file_path)

    def load_json(self, model, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

            for entry in data:
                entry = self.resolve_foreign_keys(model, entry)
                model.objects.create(**entry)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded data into {model.__name__} from {file_path}'))

    def load_csv(self, model, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                row = self.resolve_foreign_keys(model, row)
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded data into {model.__name__} from {file_path}'))

    def resolve_foreign_keys(self, model, data):
        """Converts foreign key IDs in data to actual model instances."""
        for field_name, value in list(data.items()):
            # Check if the field name ends with '_id', suggesting a foreign key
            if field_name.endswith('_id'):
                actual_field_name = field_name[:-3]  # Strip '_id' suffix to get the related field name

                # Get the related field from the model
                try:
                    field = model._meta.get_field(actual_field_name)
                    
                    # Check if this field is a ForeignKey
                    if isinstance(field, models.ForeignKey):
                        related_model = field.related_model
                        # Retrieve the related model instance by its primary key (assume `value` is the ID)
                        related_instance = related_model.objects.get(pk=value)
                        data[actual_field_name] = related_instance  # Assign the instance to the actual field
                        del data[field_name]  # Remove the `_id` version to avoid duplicate key error
                except related_model.DoesNotExist:
                    raise ValueError(f'Related instance with ID {value} not found in {related_model}')
        return data