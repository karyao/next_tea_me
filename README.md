# Django Project Template
NWHACKS 2025, Next Tea Me

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- virtualenv or venv

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <project-name>
```

2. Create and activate virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**MacOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

## Running the Project

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your browser and navigate to:
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/


## Development

### Adding New Apps

1. Create a new app in the `apps` directory:
```bash
python manage.py startapp app_name apps/app_name
```

2. Add the app to `INSTALLED_APPS` in `config/settings/base.py`:
```python
INSTALLED_APPS = [
    ...
    'apps.app_name',
]
```

## Deployment

1. Update `.env` with production settings
2. Collect static files:
```bash
python manage.py collectstatic
```
3. Set `DEBUG=False` in production
4. Configure your web server (e.g., Nginx, Apache)