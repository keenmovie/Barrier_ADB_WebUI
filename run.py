"""Entry point for the application.
In production we use a WSGI server (waitress) instead of the Flask development server.
Debug mode is disabled to avoid the warning about using a development server.
"""

from coreapp import app
from coreapp.config import Config

if __name__ == '__main__':
    try:
        from waitress import serve
        serve(app, host=Config.HOST, port=Config.PORT, threads=16, connection_limit=100)
    except Exception as e:
        app.logger.error('Failed to start waitress server: %s', e)
        # Development fallback using configured host/port
        app.run(host=Config.HOST, port=Config.PORT, debug=False)
