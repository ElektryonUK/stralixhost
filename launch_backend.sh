#!/usr/bin/env bash
set -euo pipefail

# Stralix Backend Launcher
# Usage: ./launch_backend.sh [start|stop|restart|status|logs]

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/backend"
APP_NAME="stralix-backend"
UVICORN_MODULE="app.main:app"
PORT="8000"
WORKERS="2"

cd "$APP_DIR"

cmd=${1:-start}

case "$cmd" in
  start)
    python3 -m venv .venv || true
    source .venv/bin/activate
    pip install -r requirements.txt
    mkdir -p logs
    pm2 start "uvicorn ${UVICORN_MODULE} --host 0.0.0.0 --port ${PORT} --workers ${WORKERS}" \
      --name ${APP_NAME} \
      --time \
      --env production \
      --output logs/out.log \
      --error logs/err.log
    pm2 save
    ;;
  stop)
    pm2 stop ${APP_NAME} || true
    ;;
  restart)
    pm2 restart ${APP_NAME} || pm2 start "uvicorn ${UVICORN_MODULE} --host 0.0.0.0 --port ${PORT} --workers ${WORKERS}" --name ${APP_NAME}
    pm2 save
    ;;
  status)
    pm2 status ${APP_NAME}
    ;;
  logs)
    pm2 logs ${APP_NAME}
    ;;
  *)
    echo "Unknown command: $cmd"
    echo "Usage: $0 [start|stop|restart|status|logs]"
    exit 1
    ;;
 esac
