import ktapiai_pb2
import ktapiai_pb2_grpc
import os
import datetime
import hmac
import hashlib
import mic_stream as MS # 마이크 캡처 모듈 import
import threading
import collections
import audioop
import sys

CLIENT_ID = '279a0915-44b2-411c-8aa2-ae055f33d63e'
CLIENT_KEY = 'b37807b6-0543-54e8-ac29-93a2e301cd76'
CLIENT_SECRET = 'b37807b6-0543-54e8-ac29-93a2e301cd76'

RATE = 16000
CHUNK = 1600
START_RECORD = False

class Client:
    def __init__(self):
        self._stop_event = threading.Event()
        self._requests = collections.deque()
        self._request_condition = threading.Condition()

    def _next(self):
        with self._request_condition:
            while not self._requests and not self._stop_event.is_set():
                self._request_condition.wait()
            if len(self._requests) > 0:
                return self._requests.popleft()
            else:
                raise StopIteration()

    def next(self):
        return self._next()

    def __next__(self):
        return self._next()

    def add_request(self, request):
        with self._request_condition:
            self._requests.append(request)
        self._request_condition.notify()

    def close(self):
        self._stop_event.set()
        with self._request_condition:
            self._request_condition.notify()