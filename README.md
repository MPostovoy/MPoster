# MPoster

## Queues

Работа с очередями:

```
from mposter import queues

def queues_method(data):
    print(data)

_queues = queues.Queues(threads=10, target=queues_method)
for i in range(10):
    _queues.put(i)
_queues.join()
```
Обьявление Queues, threads - Кол-во потоков, target - метод, который должен отработать.

_queues.put - Добавляем в очередь
