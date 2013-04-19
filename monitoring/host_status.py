# -*- coding: utf-8 -
from flask import render_template


def app(environ, start_response):
    """Simplest possible application object"""

    data = render_template('monitoring/templates/hosts_status.html')
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
