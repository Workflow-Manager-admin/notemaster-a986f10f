#!/bin/bash
# Start script for backend preview/fix: ensures Django settings module is always set

export DJANGO_SETTINGS_MODULE=config.settings
exec python3 manage.py runserver 0.0.0.0:8000 --noreload 2>&1 | tee server_start.log
