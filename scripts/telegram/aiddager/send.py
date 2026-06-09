#!/usr/bin/env python3
"""AI따거 그룹에 메시지 송신."""

import os
import sys
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN_KH")
CHAT_ID = -5297628070


def send(text: str) -> dict:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN_KH 환경변수가 없습니다.")
    resp = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python send.py '보낼 메시지'")
        sys.exit(1)
    result = send(" ".join(sys.argv[1:]))
    print(f"전송 완료: message_id={result['result']['message_id']}")
