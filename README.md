## Инструкция по запуску

Создаем вирутальное окружение в директории проекта и подключаемся к нему:

```bash
python3 -m venv venv
source venv/bin/activate
```

Устанавливаем необходимый модуль:

```bash
pip install build
```

Билдим python-приложение:

```bash
python -m build
```

Устанавливаем его в виртуальное окружение:

```bash
pip install dist/PyTree-0.0.1-py3-none-any.whl
```

Запускаем и оцениваем результат!)

```bash
pytree -L 2 .
```