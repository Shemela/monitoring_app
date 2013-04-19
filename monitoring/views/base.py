from flask import render_template
from flask.views import View
import settings
from urlparse import urljoin
import gevent
import urllib2
import json


class ListView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = {'objects': self.get_objects()}
        return self.render_template(context)

    def read_url(self, url):
        try:
            return urllib2.urlopen(url=url, timeout=1).read().decode("utf-8")
        except urllib2.URLError:
            return None


class IndexView(ListView):
    def get_template_name(self):
        return 'hosts_status.html'

    def get_data(self, url, path=None, out_json=False):
        work_url = urljoin(url, path) if path else url
        job = gevent.spawn(self.read_url, work_url)
        gevent.joinall([job], timeout=2)
        if out_json:
            return json.loads(job.get())
        else:
            return job.get()

    def get_objects(self):
        urls = settings.APP_HOSTS
        result = {}
        for url in urls:
            status = self.get_data(url, '/ping')
            counters = info = None
            if status:
                info = self.get_data(url=url, out_json=True)
                counters = self.get_data(url, '/counters', out_json=True)
            result[url] = {'info': info,
                           'status': status,
                           'counters': counters}
        return result

    def dispatch_request(self):
        context = {'servers': self.get_objects()}
        return self.render_template(context)


class Counters(ListView):
    def get_template_name(self):
        return 'hosts_status.html'
