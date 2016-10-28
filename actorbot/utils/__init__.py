import traceback
import importlib
from actorbot.utils import logger

def safe_import(module_name, class_name):
    if type(class_name) is list:
        for name in class_name:
            safe_import(module_name, name)
        return
    package = __package__
    if not package:
        package = __name__
    try:
        module = importlib.import_module(module_name, package)
        globals()[class_name] = getattr(module, class_name)
    except ImportError as error:
        logger.warning("Can't Import class: '%s.%s', %s",
                       module_name, class_name, error)
        logger.debug("%s", traceback.format_exc())


safe_import('.logger', 'logger')
safe_import('.logger', 'logger_init')
safe_import('.event', 'Event')
safe_import('.misc', 'print_date')
