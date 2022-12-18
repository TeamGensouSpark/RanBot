from Remilia.jsondb import db
from Remilia.lite.LiteResource import Path

resourcePath=Path("src/resources/ran_core/")
cachePath=Path("cache/")
jdb=db.JsonDB(db.File(resourcePath.abspath+"/botdb.json"),dbname="bot")