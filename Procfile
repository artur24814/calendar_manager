web: gunicorn core.wsgi
websocket: daphne -b 0.0.0.0 -p 5000 core.asgi:application