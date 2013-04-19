from flask import render_template
from flask.views import View
import settings
from urlparse import urljoin
import gevent
import urllib2

class ListView(View):

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = {'objects': self.get_objects()}
        return self.render_template(context)


class IndexView(ListView):

    def get_template_name(self):
        return 'hosts_status.html'

    def ping(self, url):
        url = urljoin(url, '/ping')
        try:
            return urllib2.urlopen(url=url, timeout=1).read()
        except urllib2.URLError:
            return None

    def get_objects(self):
        urls = settings.APP_HOSTS
        result = []
        for url in urls:
            job = gevent.spawn(urllib2.urlopen, urljoin(url, '/ping'), None, 2)
            gevent.joinall([job], timeout=2)
            try:
                status = job.get().read()
            except urllib2.URLError:
                status = None
            result.append({'url': url, 'status': status})
        return result

    def dispatch_request(self):
        context = {'servers': self.get_objects()}
        return self.render_template(context)