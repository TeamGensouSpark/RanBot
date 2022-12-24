
choices=[
'''<白羊座>
弹幕：飞符「Flying Head」（飞行之头）
使用者：赤蛮奇

被击中的话头就会像使用者一样飞出去哦。就算头
飞出去据说一段时间内还是会有意识的所以很幸运。''',
'''<金牛座>
弹幕：四天王奥义「三步必杀」
使用者：星熊勇仪

被击中的话腹部会被击穿。正常情况当然会死。但
因为是符卡所以不会死哦。很幸运啊。''',
'''<双子座>
弹幕：弦乐「风暴的合奏」
使用者：九十九姐妹

听见噩梦的旋律精神失常而死。如果刚好喜欢这种
类型的音乐的话就能够续命1。这挺幸运的。''',
'''<巨蟹座>
弹幕：变化「分福热水浴」
使用者：二岩猯藏

被击中的话会被强行蒸到恰～到好处，然后被美美
的吃掉。肯定会被嚼得骨头都不剩而死。会被一点
不留的吃干净所以很幸运♪''',
'''<狮子座>
弹幕：鵺符「弹幕奇美拉」
使用者：封兽鵺

被这个弹幕击中的话，被击中的人会变得无法辨别
真实样貌而死。不用喝酒也能使外貌变得无法辨认
这可真是幸运啊？''',
'''<处女座>
弹幕：本能「本我的解放」
使用者：古明地恋

被这个打中的话，心里的什么东西会被打开然后死
掉。在多数仍然是闭锁着的人群之中，能获得开放
不如说很幸运吧。''',
'''<天秤座>
弹幕：眼光「十七条的光芒」
使用者：丰聪耳神子

被这个击中的话会公平的被激光贯穿。当然会死就
是了，而且一般会死上17次。会死很多次所以很幸
运。''',
'''<天蝎座>
弹幕：毒符「Poison Breath」（猛毒气息）
使用者：梅蒂欣·梅兰可莉

这个要说是弹幕不如说就是纯粹的毒。肯定会十分
痛苦的死去。痛苦很久也没法马上死所以很幸运。''',
'''<射手座>
弹幕：光符「Earth Light Ray」（地球光）
使用者：雾雨魔理沙

非要说的话从身体下方被贯穿会很痛苦。而且还会
被贯穿很多次而死。首先在此之前能遇到我就很幸
运了。''',
'''<摩羯座>
弹幕：禁弹「Starbow Break」（星弧破碎）
使用者：芙兰朵露·斯卡蕾特

这家伙也是能遇到就很幸运的稀有角色。当然会有
很大可能性遭殃而死。不如说对自己使用了弹幕这
一点就够幸运了。''',
'''<水瓶座>
弹幕：怪奇「钓瓶落之怪」
使用者：琪斯美

被这个击中会脑挫伤而死。石头脑袋的话就能活下
来。但是头部会受到严重的损伤所以死了比较幸运。
好好去死吧。''',
'''<双鱼座>
弹幕：狱炎「擦弹的狱意」
使用者：克劳恩皮丝

被火焰和火焰夹在中间，蒸烤的外焦里嫩而死。能
遇到地狱的火焰这种稀有的东西真是很幸运。'''

]

introduce='''
作为天才魔法使同时也是世纪级的占卜师，
雾雨魔理沙最近发明了
完全崭新的开创性的占卜。
也就是这个「幸运弹幕占卜」。
这是把现有的星座占卜，
和我独创的弹幕占卜组合到一起的成果，
被特定的弹幕击中的话幸运就会降临，
这样的占卜。
要事先提醒的是，对被弹幕击中
所造成的伤害这边不承担任何责任。
请千万要在自己承担责任的前提下被击中。
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment,Message,MessageEvent
import random,time

divination=on_command("divination", rule=to_me(), aliases={"占卜",},priority=5)
@divination.handle()
async def handle(event:MessageEvent):
    await divination.send("占卜中...")
    time.sleep(3)
    await divination.finish(Message([MessageSegment.at(event.get_user_id()),random.choice(choices)]))

divination_intro=on_command("divination_intro", rule=to_me(), aliases={"占卜介绍",},priority=5)
@divination_intro.handle()
async def handle(event:MessageEvent):
    await divination_intro.finish(Message([MessageSegment.at(event.get_user_id()),introduce]))
    