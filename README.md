# notemaster-a986f10f

## Django Backend Preview Start Instructions

To ensure correct startup and that the `DJANGO_SETTINGS_MODULE` is configured, always use the provided start script:

```bash
cd notes_backend
./start.sh
```

If you run manage.py directly, make sure to export the environment variable first:

```bash
export DJANGO_SETTINGS_MODULE=config.settings
python3 manage.py runserver 0.0.0.0:8000
```

If you still encounter issues, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```