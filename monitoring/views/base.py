from flask import render_template
from flask.views import View
import urllib2
from monitoring.threads import CheckServers

CHECK_SERVERS = CheckServers()
CHECK_SERVERS.start()


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

    def get_objects(self):
        return CHECK_SERVERS.counters

    def dispatch_request(self):
        context = {'servers': self.get_objects()}
        return self.render_template(context)


class Counters(ListView):
    def get_template_name(self):
        return 'hosts_status.html'
