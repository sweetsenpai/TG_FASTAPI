import logging

# Цвета ANSI для терминала
COLORS = {
    "DEBUG": "\033[94m",  # синий
    "INFO": "\033[92m",  # зелёный
    "WARNING": "\033[93m",  # жёлтый
    "ERROR": "\033[91m",  # красный
    "CRITICAL": "\033[95m",  # фиолетовый
    "RESET": "\033[0m",  # сброс
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        color = COLORS.get(levelname, COLORS["RESET"])
        message = super().format(record)
        return f"{color}{message}{COLORS['RESET']}"


def setup_logger(name=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()

    base_formatter = logging.Formatter(
        fmt="[{asctime}] [{levelname}] {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )

    color_formatter = ColorFormatter(
        fmt=base_formatter._fmt, datefmt=base_formatter.datefmt, style="{"
    )

    handler.setFormatter(color_formatter)

    logger.handlers.clear()
    logger.addHandler(handler)
    return logger
