# Redis Concept Django Application

A Django application demonstrating Redis integration for caching, queuing, and real-time features.

## Overview

This project showcases how to leverage Redis with Django for:
- Caching database queries
- Message queuing
- Real-time data processing
- Session management
- Rate limiting

## Setup and Installation

1. Clone the repository
```bash
git clone <repository-url>
cd reddis_concept
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Install Redis (if not already installed)
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS with Homebrew
brew install redis
```

5. Apply migrations
```bash
python manage.py migrate
```

6. Run the development server
```bash
python manage.py runserver
```

## Project Structure

```
reddis_concept/
├── manage.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── models/
│   ├── views/
│   └── management/
│       └── commands/
│           ├── __init__.py
│           └── load_fruits.py
```

## Redis Integration Features

- **Caching**: Using Django's cache framework with Redis backend
- **Session Storage**: Configuring Redis as Django's session store
- **Queuing**: Implementing background tasks with Redis and Celery
- **Pub/Sub**: Real-time messaging with Redis channels

## Custom Django Management Commands

This project demonstrates how to create custom management commands in Django (like the `load_fruits.py` command).

### What are Custom Management Commands?

Custom management commands are extensions to Django's `manage.py` utility. They allow you to:
- Create tasks that can be executed from the command line
- Automate repetitive operations
- Schedule jobs with cron or other task schedulers
- Perform database operations or data imports/exports

### How Custom Commands Work

1. Commands live in a `management/commands` directory within a Django app
2. Each command is a Python module with a class that inherits from `BaseCommand`
3. The `handle()` method contains the logic to be executed
4. Commands can accept arguments and options

### Example Custom Command: `load_fruits`

Our `load_fruits` command demonstrates populating the database with sample fruit data:

```python
from django.core.management.base import BaseCommand
from myapp.models import Fruit

class Command(BaseCommand):
    help = 'Loads sample fruit data into the database'

    def handle(self, *args, **options):
        fruits = [
            {'name': 'Apple', 'color': 'Red', 'taste': 'Sweet'},
            {'name': 'Banana', 'color': 'Yellow', 'taste': 'Sweet'},
            {'name': 'Lemon', 'color': 'Yellow', 'taste': 'Sour'}
        ]
        
        for fruit_data in fruits:
            Fruit.objects.create(**fruit_data)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(fruits)} fruits!'))
```

### Running Custom Commands

Execute the command using:
```bash
python manage.py load_fruits
```

## Usage Examples

### Caching with Redis

```python
# In settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# In views.py
from django.core.cache import cache

def get_expensive_data(request):
    data = cache.get('expensive_data')
    if data is None:
        # Data not in cache, calculate it
        data = perform_expensive_calculation()
        # Store in cache for 1 hour (3600 seconds)
        cache.set('expensive_data', data, 3600)
    return data
```

### Creating Custom Commands

To create your own command:

1. Ensure you have a `management/commands` directory in your app
2. Create a Python file named after your command (e.g., `mycommand.py`)
3. Implement your command class:

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of what your command does'

    def add_arguments(self, parser):
        # Optional: add command-line arguments
        parser.add_argument('--optional', action='store_true', help='An optional flag')
        parser.add_argument('required_arg', type=str, help='A required argument')

    def handle(self, *args, **options):
        # Command logic goes here
        self.stdout.write(self.style.SUCCESS('Command executed successfully!'))
```

## Troubleshooting

- **Redis Connection Issues**: Ensure Redis server is running (`redis-cli ping`)
- **Command Not Found**: Verify that your app is in INSTALLED_APPS and command file is properly named
- **Caching Problems**: Check your Redis connection settings in settings.py

## License

[MIT License](LICENSE)
