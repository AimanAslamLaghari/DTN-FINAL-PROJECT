import os
import sys

# Ensure root directory is on Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from project import app

class VercelPathMiddleware:
    """WSGI Middleware to normalize PATH_INFO when Vercel rewrites requests to /api/index"""
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        # Handle /api/index or /api/index.py or /api prefix rewritten by Vercel
        if path.startswith('/api/index.py'):
            path = path[len('/api/index.py'):]
        elif path.startswith('/api/index'):
            path = path[len('/api/index'):]
        elif path.startswith('/api/') and not path.startswith('/api/services'):
            path = path[len('/api'):]
        elif path == '/api':
            path = '/'
            
        if not path or not path.startswith('/'):
            path = '/' + path
            
        environ['PATH_INFO'] = path
        return self.wsgi_app(environ, start_response)

# Apply middleware
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run()
