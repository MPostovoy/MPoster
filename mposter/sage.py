import json
import platform
import logging.handlers
from datetime import datetime
from confluent_kafka import Producer
import logging
from threading import Thread
from queue import Queue
import requests


class SageKafka(logging.Handler):
    def __init__(self, env: str, system: str, group: str, bootstrap_servers: str, project: str, level: str = 'DEBUG'):
        logging.Handler.__init__(self)
        self.bootstrap_servers = bootstrap_servers
        self.required_fields = {
            'env': env,
            'group': group,
            'system': system,
            # 'project': project,
            'inst': platform.uname()[1],
        }
        self.topic = f'sage-logs-{group}'
        self.project = project
        self._producer = Producer(
            {'bootstrap.servers': self.bootstrap_servers,
             'client.id': f'{group}_logs'}
        )

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {self.topic} - {msg.topic()} [{msg.partition()}]')

    def emit(self, dst_info):
        try:
            _level = dst_info.msg.split('|')[1]
            _msg = dst_info.msg.split('|', 2)[2].split(' - ', 1)[1]

            _data = {'project': self.project, 'logger_level': _level.strip(), 'msg': _msg}

            send_info = self.required_fields.copy()
            send_info.update(_data)

            if 'extra' in dst_info.extra and dst_info.extra['extra'] is not None:
                send_info.update(dst_info.extra['extra'])

            send_info["@timestamp"] = datetime.utcnow().isoformat()[:-3] + 'Z'

            self._producer.produce(self.topic, json.dumps(send_info), callback=self.delivery_report)
            self._producer.poll(0.1)

        except BufferError as e:
            print('BufferError', e)
            self._producer.poll(2)
            self._producer.flush()

        except Exception as e:
            print('Exception', e)
            self._producer.poll(0.1)

    def close(self):
        self._producer.flush()
        logging.Handler.close(self)


class SageRest(logging.Handler):
    def __init__(self, env: str, system: str, group: str, project: str, host: str, level: str = 'DEBUG'):
        logging.Handler.__init__(self)

        self.required_fields = {
            'env': env,
            'group': group,
            'system': system,
            # 'project': project,
            'inst': platform.uname()[1],
        }
        self.topic = f'sage-logs-{group}'
        self.project = project
        self.host = host
        self.queues = Queue()
        self.create_q()

    def _send_text(self, idx, queue):
        while True:
            try:
                data = queue.get()
                r = requests.post(self.host, timeout=1, data={'msg': json.dumps(data)})
                print(r)
            except Exception as ex:
                print('send_text', ex)

            finally:
                queue.task_done()

    def create_q(self):
        for idx in range(5):
            worker = Thread(target=self._send_text, args=(idx, self.queues))
            worker.setDaemon(True)
            worker.start()

    def emit(self, dst_info):
        try:
            _level = dst_info.msg.split('|')[1]
            _msg = dst_info.msg.split('|', 2)[2].split(' - ', 1)[1]

            _data = {'project': self.project, 'logger_level': _level.strip(), 'msg': _msg}

            send_info = self.required_fields.copy()
            send_info.update(_data)

            if 'extra' in dst_info.extra and dst_info.extra['extra'] is not None:
                send_info.update(dst_info.extra['extra'])

            send_info["@timestamp"] = datetime.utcnow().isoformat()[:-3] + 'Z'
            self.queues.put(send_info)

        except Exception as e:
            print(e)

    def close(self):
        self.queues.join()
        logging.Handler.close(self)
