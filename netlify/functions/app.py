import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import app

def handler(event, context):
    from werkzeug.wrappers import Request, Response
    from werkzeug.serving import WSGIRequestHandler
    import io
    
    # Simple WSGI wrapper for Netlify
    environ = {
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event['path'],
        'QUERY_STRING': event.get('rawQuery', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': str(len(event.get('body', ''))),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '8000',
        'wsgi.input': io.BytesIO(event.get('body', '').encode()),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https'
    }
    
    # Add headers to environ
    for key, value in event.get('headers', {}).items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    response_data = []
    def start_response(status, headers):
        response_data.extend([status, headers])
    
    result = app(environ, start_response)
    
    return {
        'statusCode': int(response_data[0].split()[0]),
        'headers': dict(response_data[1]),
        'body': ''.join(result)
    }