# Задача №3: декоратор `timed_logged`

## Реализовать декоратор, который будет:

- Измерять время выполнения функции в миллисекундах.
- Выводить имя, аргументы, результат и время выполнения.
- При ошибке логировать её тип и сообщение, не скрывая исключение.
- Работать с любыми сигнатурами (`*args`, `**kwargs`).
- Сохранять метаданные функции (`__name__`, `__doc__`) через `functools.wraps`.

## Пример использования

```python
from time import sleep

from timed_logged import timed_logged


@timed_logged
def slow_sum(a, b, delay=0.5):
    sleep(delay)
    return a + b


slow_sum(1, 2, delay=0.2)
```

## Решение

- `timed_logged.py` — декоратор и запись фактического времени каждого вызова.
- `random_sleep.py` — демонстрация ручной и случайной задержки. Ручное значение задаётся в секундах; случайный режим выбирает задержку до 0,06 секунды.
- `benchmark.py` — запускает серии из 5, 25, 50, 100, 500 и 5 000 вызовов, строит KDE-график и сохраняет лог.
- `example.py` — пример `slow_sum` из условия; перед вызовом просит ввести длительность ожидания в секундах.

График сохраняется в `artifacts/runtime_distribution.png`, лог бенчмарка — в `artifacts/benchmark.log`. Серия из 5 680 вызовов выполняется несколько минут из-за реального `sleep`.

## Запуск

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python benchmark.py
.venv/bin/python random_sleep.py
.venv/bin/python example.py
.venv/bin/python -m unittest
```

При запуске `example.py` введи, например, `0.2`, чтобы функция ждала 0,2 секунды.

`random_sleep.py` попросит ввести длительность в секундах. Случайный режим можно вызвать из Python:

```python
from random_sleep import random_sleep

random_sleep(use_random_val=True)
```
