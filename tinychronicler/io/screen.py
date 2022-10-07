from loguru import logger
from screeninfo import ScreenInfoError, get_monitors


def get_screen_dimensions():
    results = []
    try:
        for monitor in get_monitors():
            results.append({
                "x": monitor.x,
                "y": monitor.y,
                "width": monitor.width,
                "height": monitor.height,
            })
    except ScreenInfoError:
        logger.error("Could not retreive monitor dimensions")
    return results
