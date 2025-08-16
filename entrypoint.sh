#!/bin/sh

# Run Alembic migrations
# alembic upgrade head

# Start Uvicorn server
cd src && uvicorn app:app --host 0.0.0.0 --port 8080 --reload --log-config ../logging.yaml
