#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server"
  python3 manage.py runserver 0.0.0.0:5000
  python3 mainloop.py
else
  echo "Running Production Server"
  python3 manage.py runserver 0.0.0.0:5000
fi
