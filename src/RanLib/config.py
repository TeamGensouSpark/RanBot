from nonebot import get_driver
from Remilia.base.typings import T
driver = get_driver()
config = driver.config


def getElse(key: str, elsevalue:T=None) -> T:
    return getattr(config, key) if hasattr(config, key) else elsevalue
