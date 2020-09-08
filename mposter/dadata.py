import zeep
import time


class DaData(object):
    def __init__(self, host: str):
        self._host = host

    def get_data(self, address: str, errors: int = 0, max_errors: int = 3):
        while errors < max_errors:
            try:
                _client = zeep.Client(self._host)
                _response = _client.service.getAddress(input=address)
                return _response

            except Exception as ex:
                print(ex)
                errors += 1
                time.sleep(2)
