"""PII 정규식 정밀도 검증 (false positive · false negative)."""
import re

EMAIL = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_KOREA = r'\d{2,3}-\d{3,4}-\d{4}'
RRN = r'\d{6}-\d{7}'


def test_email_detect_positive():
    cases = ["test@example.com", "user.name+tag@sub.domain.co.kr", "a@b.co"]
    for c in cases:
        assert re.search(EMAIL, f"text {c} text"), f"email not detected: {c}"


def test_email_false_positive():
    """일반 텍스트가 email 로 잘못 인식되지 않는지."""
    cases = ["hello world", "no-email-here", "5 < 10"]
    for c in cases:
        assert not re.search(EMAIL, c), f"false positive on: {c}"


def test_phone_korea_detect():
    cases = ["010-1234-5678", "02-123-4567", "031-1234-5678"]
    for c in cases:
        assert re.search(PHONE_KOREA, c), f"phone not detected: {c}"


def test_rrn_detect():
    cases = ["123456-1234567", "990101-2345678"]
    for c in cases:
        assert re.search(RRN, c), f"rrn not detected: {c}"


def test_rrn_false_positive_short():
    """잘못된 형식 (5자리 등) 은 detect 안 함."""
    assert not re.search(RRN, "12345-1234567"), "rrn pattern matched 5-digit prefix"


def test_combined_pii_in_text():
    """한 문장에 여러 PII 가 섞여 있을 때 모두 detect."""
    text = "이메일 test@example.com, 전화 010-1234-5678, 주민번호 990101-1234567"
    assert re.search(EMAIL, text)
    assert re.search(PHONE_KOREA, text)
    assert re.search(RRN, text)
