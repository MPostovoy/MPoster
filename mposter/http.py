import random
import requests


def get_proxies(errors: int = -1, paid_errors: int = 5, paid_type: int = -1,
                paid_host: str = 'http://88.198.167.20:8083/proxies?', paid_max_proxies: int = 12054,
                vpn: bool = False, vpn_errors: int = 7,
                tor_min_proxies: int = 8120, tor_max_proxies: int = 8191) -> dict:
    try:
        if errors < paid_errors:
            _proxies = requests.get(f'{paid_host}type={paid_type}', timeout=1).json()
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
