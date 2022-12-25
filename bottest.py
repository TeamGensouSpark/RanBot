from typing import TYPE_CHECKING, Set
import bottest

if TYPE_CHECKING:
    from nonebot.plugin import Plugin


@bottest.fixture
def load_plugins(nonebug_init: None) -> Set["Plugin"]:
    import nonebot
    return nonebot.load_plugins("src/plugins")