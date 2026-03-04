import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logger(name: str = "ai_code_intel"):
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )
    logger = logging.getLogger(name)
    return logger

logger = setup_logger()
