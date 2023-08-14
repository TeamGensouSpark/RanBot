from Remilia.sdb import YamlStruct,DataBase

BotDB = DataBase("src/RanBot/resources/DataBase",YamlStruct)

CateRanCore = BotDB.getCate("RanCore")