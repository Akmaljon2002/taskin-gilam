import base64
from typing import List, Union
from fastapi import HTTPException
from pydantic import BaseModel
from random import choices
import requests
import json


class SendSmsRequest(BaseModel):
    m_to: Union[str, List[str]]
    m_text: str


def generate_random_string(length: int) -> str:
    return ''.join(choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))


async def send_sms(m_to: Union[str, List[str]], m_text: str):
    AUTH = "Basic " + base64.b64encode(b"taskin:8kR45xxT2B").decode()
    URL = "http://91.204.239.44/broker-api/send"
    ORIGINATOR = "3700"

    if isinstance(m_to, str):
        sent_sms_count = 1
        m_id = generate_random_string(12)
        postdata = json.dumps({
            "messages": [
                {
                    "recipient": m_to,
                    "message-id": m_id,
                    "sms": {
                        "originator": ORIGINATOR,
                        "content": {"text": m_text}
                    }
                }
            ]
        })
    elif isinstance(m_to, list):
        sent_sms_count = len(m_to)
        messages = []
        for one_phone in m_to:
            m_id = generate_random_string(12)
            messages.append({
                "recipient": one_phone,
                "message-id": m_id
            })
        postdata = json.dumps({
            "priority": "",
            "sms": {
                "originator": ORIGINATOR,
                "content": {"text": m_text}
            },
            "messages": messages
        })
    else:
        raise HTTPException(status_code=400, detail="Invalid 'm_to' type")

    headers = {
        "Authorization": AUTH,
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, headers=headers, data=postdata)
        if response.text == "Request is received":
            return {"status": "success", "sent_sms_count": sent_sms_count}
        else:
            return {"status": "error", "message": "Failed to send SMS"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
