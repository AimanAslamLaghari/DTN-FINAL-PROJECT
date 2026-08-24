import os
import sys

# Ensure root directory is on Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from project import app

class VercelPathMiddleware:
    """WSGI Middleware to normalize PATH_INFO and preserve static/dynamic routes on Vercel"""
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # Retrieve actual request path from Vercel headers if rewritten
        raw_path = environ.get('RAW_URI') or environ.get('REQUEST_URI') or environ.get('HTTP_X_FORWARDED_PATH') or ''
        if raw_path:
            path = raw_path.split('?')[0]
        else:
            path = environ.get('PATH_INFO', '')

        # Normalize /api/index prefixes if present
        if path.startswith('/api/index.py'):
            path = path[len('/api/index.py'):]
        elif path.startswith('/api/index'):
            path = path[len('/api/index'):]

        if not path or not path.startswith('/'):
            path = '/' + path

        environ['PATH_INFO'] = path
        return self.wsgi_app(environ, start_response)

# Apply middleware
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run()
