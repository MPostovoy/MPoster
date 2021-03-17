from user_agent import generate_user_agent
from loguru import logger
import requests
import random
import time
import sys


def get_proxies(errors: int = -1, paid_errors: int = 5, paid_type: int = -1, paid_check_host: str = '',
                paid_host: str = 'http://88.198.167.20:8083/proxies?', paid_max_proxies: int = 12127,
                vpn: bool = False, vpn_errors: int = 25,
                tor_min_proxies: int = 8120, tor_max_proxies: int = 8191) -> dict:
    try:
        if errors < paid_errors:
            _proxies = requests.get(f'{paid_host}type={paid_type}&host={paid_check_host}', timeout=1).json()
            return _proxies
        elif paid_errors <= errors < vpn_errors and vpn:
            return {'http': 'http://crawlers:Z3WqSbWQaKGxb9eTvEyYC2kS2W4DHwUM1FfTwikF@167.86.80.177:8889',
                    'https': 'http://crawlers:Z3WqSbWQaKGxb9eTvEyYC2kS2W4DHwUM1FfTwikF@167.86.80.177:8889'}
        else:
            _port: int = random.randrange(tor_min_proxies, tor_max_proxies)
            return {'http': f'http://88.198.167.20:{_port}',
                    'https': f'http://88.198.167.20:{_port}'}

    except Exception:
        _port = random.randint(12000, paid_max_proxies)
        _proxies = {"http": f"http://do-worker01p.sn-offline.com:{_port}",
                    "https": f"http://do-worker01p.sn-offline.com:{_port}"}
        return _proxies


def request(method: str, link: str, timeout: int = 7, verify: bool = True, data: dict = None, json=None,
            max_errors: int = 6, proxies: dict = None, proxies_vpn: bool = True, paid_errors: int = 4,
            paid_check_host: str = '', continue_status: bool = True, headers: dict = None,
            session=None):
    _errors: int = 0
    while _errors < max_errors:
        try:
            if proxies is None:
                _proxies: dict = get_proxies(_errors, paid_host='http://vm-additional-services02p:8083/proxies?',
                                             paid_errors=paid_errors, vpn=proxies_vpn, paid_check_host=paid_check_host)
            else:
                _proxies = proxies

            logger.info(f'REQUEST: {method} request to: {link} (proxies: {_proxies}), errors: {_errors}/{max_errors}')

            if headers is None:
                headers = {'User-Agent': generate_user_agent()}
            else:
                headers['User-Agent'] = generate_user_agent()

            if session is None:
                _response = requests.request(method, link, proxies=_proxies, timeout=timeout, verify=verify, data=data,
                                             json=json, headers=headers)
            else:
                _response = session.request(method, link, proxies=_proxies, timeout=timeout, verify=verify, data=data,
                                            json=json, headers=headers)

            logger.info(f'REQUEST: {method} response to: {link} (proxies: {_proxies}), '
                        f'status code: {_response.status_code}')

            if continue_status and _response.status_code != 200:
                _errors += 1
                continue

            return _response
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f'REQUEST: {method} response to: {link}, exception: {exc_tb.tb_lineno}.{ex}')
            _errors += 1


def parsing_headers(text: str):
    _data: list = text.split('\n')
    if len(_data) < 2:
        return None

    _headers: dict = dict()
    for line in _data:
        line = line.split(': ', 1)
        if len(line) < 2:
            continue

        _headers[line[0]] = line[1]

    return _headers


class Fuck_proxies(object):
    def __init__(self, timeout: int = 90):
        self.proxies = dict()
        self.timeout = timeout

    def check_proxy(self, proxy: str):
        if proxy in self.proxies:
            if int(time.time()) - self.proxies[proxy] < self.timeout:

                logger.info(f'FUCK PROXIES: len proxies: {len(self.proxies)}')
                return True
            else:
                del self.proxies[proxy]
        return False

    def add(self, proxy: str):
        self.proxies[proxy] = int(time.time())
        logger.info(f'FUCK PROXIES: {proxy} add to fuck_proxies, len: {len(self.proxies)}')
