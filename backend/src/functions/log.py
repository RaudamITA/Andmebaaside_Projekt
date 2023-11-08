from datetime import datetime
from database.models import Log


async def log(who, what, status, db):
    now = datetime.now()
    print(who, what, now, status)
    db.add(Log(who=who, what=what, when=now, status=status))
    db.commit()
