import threading
from monitoring.utils import get_objects
from settings import APP_HOSTS, UPDATE_TIME
import settings


class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.counters = []

    def get_qps(self, url, result):
        counters = self.counters[url]['counters']
        if url in self.counters:
            for counter in result.keys():
                if counter in counters.keys():
                    result[counter]['qps'] = float(result[counter]['count'] - counters[counter]['count'])/settings.UPDATE_TIME
        return result

    def run(self):
        while not self.event.is_set():
            output = {}
            urls = APP_HOSTS
            for url in urls:
                result = get_objects(url)
                if result['status'] and len(self.counters):
                    result['counters'] = self.get_qps(url, result['counters'])
                output[url] = result
            self.counters = output
            self.event.wait(UPDATE_TIME)


    def stop(self):
        self.event.set()

{'url': {
    12: {'count': 473737, 'delta': 1},
    13: {},
    14: {},
    'status': 'OK'
    }}