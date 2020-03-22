import uuid
from datetime import datetime
from ..services import ddb
from ..services import util, statsd

@statsd.statsd_root_stats
def add(user_id, message_text):
    msg_id = str(uuid.uuid4())
    dt = datetime.utcnow().isoformat()
    item = {
        'id': msg_id,
        'datetime': dt,
        'user_id': user_id,
        'message_text': message_text,
    }
    return ddb.put(ddb.MESSAGES, item)

@statsd.statsd_root_stats
def get_all():
    return ddb.scan(ddb.MESSAGES, sort='datetime')

'''
def add(pid, dt, uid, todo):
    if ddbddb_todos_add_todo(pid, dt, uid, todo):
        return True
    return False

def get():
    return aws.ddb_todos_get_all()
'''