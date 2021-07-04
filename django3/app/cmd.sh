#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
  echo "Running Development Server"
  nohup python3 mainloop.py &
  python3 manage.py runserver 0.0.0.0:5000
  
else
  echo "Running Production Server"
  nohup python3 mainloop.py &
  python3 manage.py runserver 0.0.0.0:5000
fi
