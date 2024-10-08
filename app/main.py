from google.appengine.api import wrap_wsgi_app
from conf.wsgi import application

app = wrap_wsgi_app(application)
