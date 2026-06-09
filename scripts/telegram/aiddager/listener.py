#!/usr/bin/env python3
"""AI따거 그룹 메시지 listener daemon. 새 메시지를 polling해서 로컬에 저장."""

import os
import json
import time
import requests
from datetime import datetime

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN_KH")
CHAT_ID = -5297628070
OFFSET_FILE = os.path.join(os.path.dirname(__file__), ".offset")
LOG_FILE = os.path.join(os.path.dirname(__file__), "messages.jsonl")
POLL_INTERVAL = 3  # seconds


def get_offset() -> int:
    if os.path.exists(OFFSET_FILE):
        return int(open(OFFSET_FILE).read().strip())
    return 0


def save_offset(offset: int):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))


def poll():
    offset = get_offset()
    resp = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
        params={"offset": offset, "timeout": 30},
        timeout=40,
    )
    resp.raise_for_status()
    updates = resp.json().get("result", [])
    new_messages = []
    for u in updates:
        msg = u.get("message", {})
        if msg.get("chat", {}).get("id") == CHAT_ID:
            entry = {
                "update_id": u["update_id"],
                "from": msg.get("from", {}).get("first_name", "unknown"),
                "text": msg.get("text", ""),
                "date": msg.get("date"),
                "received_at": datetime.now().isoformat(),
            }
            new_messages.append(entry)
            print(f"[{entry['from']}] {entry['text']}")
    if new_messages:
        with open(LOG_FILE, "a") as f:
            for m in new_messages:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")
    if updates:
        save_offset(updates[-1]["update_id"] + 1)
    return len(new_messages)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN_KH 환경변수가 없습니다.")
    print(f"AI따거 listener 시작 (chat_id={CHAT_ID})")
    while True:
        try:
            count = poll()
            if count:
                print(f"  → {count}개 저장됨")
        except Exception as e:
            print(f"[오류] {e}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
