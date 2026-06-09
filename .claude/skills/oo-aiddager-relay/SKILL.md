# Skill: oo-aiddager-relay

AI따거 텔레그램 그룹과 Claude Code 간 송수신 relay.

## Trigger 키워드

다음 발화 중 하나가 나오면 이 skill 을 활성화한다:

1. "따거에 보내줘"
2. "따거 보내"
3. "텔레그램 보내"
4. "AI따거 전송"
5. "따거에 전달"
6. "그룹에 보내줘"
7. "따거 읽어줘"
8. "따거 확인"
9. "텔레그램 확인"
10. "따거 메시지"
11. "새 메시지 확인"
12. "그룹 메시지 읽어"
13. "listener 시작"
14. "텔레그램 대기"

## 송신 (send)

trigger: "따거에 보내줘", "텔레그램 보내" 등

```bash
source ~/.zshrc && python /Users/data1/lab/aaio-mine/scripts/telegram/aiddager/send.py "메시지 내용"
```

## 수신 / 읽기 (read)

trigger: "따거 읽어줘", "따거 확인", "새 메시지 확인" 등

```bash
source ~/.zshrc && python /Users/data1/lab/aaio-mine/scripts/telegram/aiddager/read.py
```

## Listener daemon 시작

trigger: "listener 시작", "텔레그램 대기"

```bash
source ~/.zshrc && python /Users/data1/lab/aaio-mine/scripts/telegram/aiddager/listener.py
```

## 파일 위치

| 파일 | 역할 |
|------|------|
| `scripts/telegram/aiddager/send.py` | 그룹 메시지 송신 |
| `scripts/telegram/aiddager/read.py` | 최근 메시지 읽기 |
| `scripts/telegram/aiddager/listener.py` | 실시간 polling daemon |
| `scripts/telegram/aiddager/messages.jsonl` | 수신 메시지 로그 (gitignored) |

## 환경변수

- `TELEGRAM_BOT_TOKEN_KH` — ~/.zshrc 에 등록됨
