from fastapi import APIRouter, Header
from pydantic import BaseModel
from ..services import util, messages, statsd

router = APIRouter()


@router.get("/")
@statsd.statsd_root_stats
def get():
    return messages.get_all() 

class Message(BaseModel):
    text: str

@router.post("/add")
@statsd.statsd_root_stats
def add(message: Message, authorization: str = Header(None)):
    #util.logger.warning(f"Authorization Header: {authorization}")
    user_id = util.get_user_data_from_token(authorization).get('sub')
    #util.logger.warning(f"User ID: {user_id}")
    response = messages.add(user_id, message.text)
    return {"msg": response}
