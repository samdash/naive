#!/bin/bash

NAME="naive"
FLASKDIR=/Users/xxxx/Documents/flask_app
VENVDIR=/Users/xxxx/Documents/flask_app/flask_env
SOCKFILE=/Users/xxxx/Documents/flask_app/sock
USER=naive
GROUP=naive
NUM_WORKERS=3

echo "Starting $NAME"

# activate the virtualenv
cd $VENVDIR
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your unicorn
exec gunicorn -k gevent app:app -b 127.0.0.1:8000 \
  --name $NAME \
  --workers $NUM_WORKERS \
#  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE