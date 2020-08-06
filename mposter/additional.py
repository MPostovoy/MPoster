import time
import requests


def write_result(path: str, result, type_w: str = 'a', errors: int = 0):
    while errors < 3:
        try:
            with open(path, type_w, encoding='utf-8') as f:
                if type_w == 'a':
                    f.write(f'{result}\n')
                else:
                    f.write(f'{result}')
                return None

        except Exception:
            errors += 1
            time.sleep(1)
            continue


def update_monitoring(crawler: str, reply: str, status: int = 1, host: str = 'localhost'):
    try:
        requests.get(f'http://{host}/api/v1/crawlers/reply?'
                     f'crawler_name={crawler}&status={status}&reply={reply}', timeout=0.1)
    except Exception:
        pass
