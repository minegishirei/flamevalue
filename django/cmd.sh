#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server"
else
  echo "Running Production Server"
  #exec python3 manage.py runserver 0.0.0.0:5000 
fi
