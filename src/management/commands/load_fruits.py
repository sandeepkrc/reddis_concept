import json
from django.core.management.base import BaseCommand
from src.models import Fruit

class Command(BaseCommand):
    help = 'Load fruits data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        
        try:
            with open(json_file_path, 'r') as file:
                fruits_data = json.load(file)
                
            # Clear existing data (optional)
            Fruit.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing fruits data'))
            
            # Create new fruits from JSON data
            fruits_created = 0
            for fruit_item in fruits_data:
                Fruit.objects.create(name=fruit_item['name'])
                fruits_created += 1
                
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded {fruits_created} fruits from {json_file_path}')
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {json_file_path}')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON in file: {json_file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading data: {str(e)}')
            )
