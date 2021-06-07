import time
import requests
import platform


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
        _node = platform.node()

        if _node in 'vm-additional-services02p.tcsbank.ru':
            host = 'localhost:8100'
        elif _node in 'm1-crawlig-portal-1.tcsbank.ru':
            host = 'localhost'

        requests.get(f'http://{host}/api/v1/crawlers/reply?'
                     f'crawler_name={crawler}&status={status}&reply={reply}', timeout=0.1)
    except Exception:
        pass


def strip(text):
    return text.replace('\n', '').strip().replace(u'\xa0', ' ').replace('  ', '')


def find(text, start, end):
    start_idx = text.find(start)
    if start_idx < 1:
        return ''

    text = text[start_idx + len(start):]
    end_idx = text.find(end)
    if end_idx < 1:
        return ''

    text = text[:end_idx]
    return text
