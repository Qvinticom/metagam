import urllib
import string
import re
import cgi
import datetime
import calendar

re_color = re.compile(r'^([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$', re.IGNORECASE)
re_human_time = re.compile(r'^(\d\d)\.(\d\d)\.(\d\d\d\d)(?:| (\d\d:\d\d:\d\d))$')
re_valid_nonnegative_int = re.compile(r'^[0-9]+$')
re_datetime = re.compile(r'^(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)$')
re_date = re.compile(r'^(\d\d\d\d)-(\d\d)-(\d\d)')

def urldecode(str):
    if str is None:
        return ""
    return urllib.unquote(str).decode("utf-8")

def urlencode(str):
    if str is None:
        return ""
    if type(str) == unicode:
        str = str.encode("utf-8")
    return urllib.quote(str)

def intz(str, onerror=0):
    try:
        return int(str)
    except (ValueError, TypeError):
        return onerror

def floatz(str, onerror=0):
    try:
        return float(str)
    except (ValueError, TypeError):
        return onerror

def valid_nonnegative_int(str):
    return re_valid_nonnegative_int.match(str)

def jsencode(val):
    if val is None:
        return ""
    if type(val) != type("") and type(val) != unicode:
        val = str(val)
    val = string.replace(val, "\\", "\\\\")
    val = string.replace(val, "'", "\\'")
    val = string.replace(val, "\r", "\\r")
    val = string.replace(val, "\n", "\\n")
    return val

def jsdecode(val):
    if val is None:
        return ""
    if type(val) != type("") and type(val) != unicode:
        val = str(val)
    val = string.replace(val, "\\n", "\n")
    val = string.replace(val, "\\r", "\r")
    val = string.replace(val, "\\'", "'")
    val = string.replace(val, "\\\\", "\\")
    return val

def format_gender(gender, str):
    return re.sub(r'\[gender\?([^:\]]*):([^:\]]*)\]', lambda m: m.group(1) if gender == 1 or gender == "1" else m.group(2), str)

def parse_color(color):
    m = re_color.match(color)
    if not m:
        return None
    r, g, b = m.group(1, 2, 3)
    return (int(r, 16), int(g, 16), int(b, 16))

def htmlescape(val):
    if val is None:
        return ""
    if type(val) != type("") and type(val) != unicode:
        val = str(val)
    val = string.replace(val, "&", "&amp;")
    val = string.replace(val, '"', "&quot;")
    val = string.replace(val, "<", "&lt;")
    val = string.replace(val, ">", "&gt;")
    return val

def htmldecode(val):
    if val is None:
        return ""
    if type(val) != type("") and type(val) != unicode:
        val = str(val)
    val = string.replace(val, "&quot;", '"')
    val = string.replace(val, "&lt;", "<")
    val = string.replace(val, "&gt;", ">")
    val = string.replace(val, "&amp;", "&")
    return val

def from_unixtime(ts):
    return datetime.datetime.utcfromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")

def unix_timestamp(val):
    m = re_datetime.match(val)
    if m:
        y, m, d, hh, mm, ss = m.group(1, 2, 3, 4, 5, 6)
    else:
        m = re_date.match(val)
        if m:
            y, m, d = m.group(1, 2, 3)
            hh = 0
            mm = 0
            ss = 0
        else:
            return None
    return calendar.timegm(datetime.datetime(int(y), int(m), int(d), int(hh), int(mm), int(ss), tzinfo=None).utctimetuple())

def datetime_to_human(str):
    m = re_datetime.match(str)
    if not m:
        return None
    y, m, d, hh, mm, ss = m.group(1, 2, 3, 4, 5, 6)
    return "%02d.%02d.%04d %02d:%02d:%02d" % (int(d), int(m), int(y), int(hh), int(mm), int(ss))

def date_to_human(str):
    m = re_date.match(str)
    if not m:
        return None
    y, m, d = m.group(1, 2, 3)
    return "%02d.%02d.%04d" % (int(d), int(m), int(y))

def date_from_human(str):
    m = re_human_time.match(str)
    if not m:
        return None
    d, m, y, t = m.group(1, 2, 3, 4)
    return "%04d-%02d-%02d %s" % (int(y), int(m), int(d), t if t else "00:00:00")

