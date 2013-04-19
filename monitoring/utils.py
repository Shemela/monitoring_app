import json
import urllib2
from urlparse import urljoin

import gevent


def read_url(url):
    try:
        return urllib2.urlopen(url=url, timeout=1).read().decode("utf-8")
    except urllib2.URLError:
        return None


def get_data(url, path=None, out_json=False):
    work_url = urljoin(url, path) if path else url
    job = gevent.spawn(read_url, work_url)
    gevent.joinall([job], timeout=2)
    if out_json:
        return json.loads(job.get())
    else:
        return job.get()


def get_objects(url):
    result = {'counters': {}}
    status = get_data(url, '/ping')
    info = None
    if status:
        info = get_data(url=url, out_json=True)
        counters = get_data(url, '/counters', out_json=True)
        for counter in counters:
            info_count = get_data(url, '/counters/{0}'.format(counter), out_json=True)
            result['counters'][counter] = info_count['response_served']
    result['info'] = info
    result['status'] = status
    return result
