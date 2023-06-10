import logging
import sys

import structlog
from aiologger import Logger
from aiologger.handlers.base import Handler
from structlog._config import BoundLoggerLazyProxy

from adapter import BoundLoggerAdapter
from handlers import ConsoleHandler
from handlers import GraylogHandler
from handlers import MockHandler

PROXY_LOGGER = Logger()

# Необходимо если не будет установлен ни один хендлер - raise Exception("No handlers could be found for logger")
PROXY_LOGGER.add_handler(MockHandler())

# Быть осторожным с подключаемыми процессами т.к. может изменить главный словарь со всем контекстом.
# Мутацию данных лучше произвести в adapter.py
structlog.configure(
    logger_factory=lambda: PROXY_LOGGER,  # Для использования handlers aiologger
    wrapper_class=BoundLoggerAdapter,  # Для использования интерфейса structlog и проксирования в aiologger
    processors=[],  # Кастомизация лога, если не указать пустой список, добавятся стандартные форматеры.
)


def console_handler(level: str = "DEBUG", fields: list[str] = None) -> ConsoleHandler:
    """Консольный обработчик aiologger.AsyncStreamHandler."""

    return ConsoleHandler(
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
        formatter=None,
        filter=None,
        fields=fields,
    )


def graylog_handler(host: str, port: int, level: str = "DEBUG") -> GraylogHandler:
    """Обработчик для отправки логов в Graylog через UDP."""

    return GraylogHandler(host=host, port=port, level=getattr(logging, level.upper()))


def add_handler(handler: Handler) -> None:
    """Добавление обработчика логов в proxy logger."""

    PROXY_LOGGER.add_handler(handler)


def get_logger(logger: BoundLoggerLazyProxy = None, **kwargs) -> BoundLoggerLazyProxy:
    """Инициализация лога."""

    initial_values = dict()

    if logger:
        initial_values.update(**logger._initial_values)

    initial_values.update(**kwargs)

    return structlog.get_logger(**initial_values)
