from typing import TYPE_CHECKING, Set
from Remilia.lite.LiteLog import Logger,DefaultStyle
import pytest

logger=Logger(__name__,DefaultStyle.default_LogStyle1)

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

logger.info("start import test")

@pytest.fixture
def load_plugins(nonebug_init: None) -> Set["Plugin"]:
    import nonebot
    return nonebot.load_plugins("src/plugins")

logger.info("import test finish,no error")