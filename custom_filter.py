import re
from datetime import datetime, timedelta, timezone


def custom_filter(value: str, offset: int = 0) -> str:
    """ISO形式の日時文字列を、UTCから offset 分ずらしたタイムゾーンのISO形式に変換する

    Python 3.9 の fromisoformat() は秒未満が3桁または6桁の場合しか解析できないため、
    秒未満の桁数を次のようにそろえてから解析し、出力も同じ桁数にする。
      - 1〜3桁: 3桁（ミリ秒）に0埋め
      - 4〜6桁: 6桁（マイクロ秒）に0埋め
      - 7桁以上: 6桁に切り捨て
      - 秒未満なし: 秒まで出力
    """
    s = str(value)
    timespec = 'auto'
    m = re.search(r'\.(\d+)', s)
    if m:
        digits = 3 if len(m.group(1)) <= 3 else 6
        frac = m.group(1).ljust(digits, '0')[:digits]
        s = s[:m.start()] + '.' + frac + s[m.end():]
        timespec = 'milliseconds' if digits == 3 else 'microseconds'
    s = s.replace('Z', '+00:00')
    tz = timezone(timedelta(minutes=int(offset)))
    return datetime.fromisoformat(s).astimezone(tz).isoformat(timespec=timespec)


class FilterModule(object):
    def filters(self):
        return {'custom_filter': custom_filter}
