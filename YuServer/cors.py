from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None, allow_credentials=True,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
  if methods is not None:
    methods = ', '.join(sorted(x.upper() for x in methods))
  if headers is not None and not isinstance(headers, basestring):
    headers = ', '.join(x.upper() for x in headers)
  if not isinstance(origin, basestring):
    origin = ', '.join(origin)
  if isinstance(max_age, timedelta):
    max_age = max_age.total_seconds()

  def get_methods():
    if methods is not None:
      return methods

    options_resp = current_app.make_default_options_response()
    return options_resp.headers['allow']

  def decorator(func):
    def wrapped_function(*args, **kwargs):
      if automatic_options and request.method == 'OPTIONS':
        resp = current_app.make_default_options_response()
      else:
        resp = make_response(func(*args, **kwargs))
      if not attach_to_all and request.method != 'OPTIONS':
        return resp

      resp_headers = resp.headers

      resp_headers['Access-Control-Allow-Origin'] = origin
      resp_headers['Access-Control-Allow-Methods'] = get_methods()
      resp_headers['Access-Control-Max-Age'] = str(max_age)
      if headers is not None:
        resp_headers['Access-Control-Allow-Headers'] = headers
      if allow_credentials:
        resp_headers['Access-Control-Allow-Credentials'] = 'true'
      resp_headers['p3p'] = 'CP="This is not p3p policy!"'
      return resp

    func.provide_automatic_options = False
    return update_wrapper(wrapped_function, func)
  return decorator
