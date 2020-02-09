#!/usr/bin/env sh

python -m flask db upgrade
/usr/local/bin/gunicorn "${FLASK_APP_MODULE}" --log-level INFO --preload -b "0.0.0.0:${FLASK_PORT}" --access-logfile - --error-logfile - --capture-output --keyfile "${SERVER_KEY}" --certfile "${SERVER_CRT}" --ca-certs "${SERVER_CA_CRT}" --ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384"
