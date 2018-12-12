# -*- coding: UTF-8 -*-
import sys
import re


def LongToInt(value):  # 由于int+int超出范围后自动转为long型，通过这个转回来
    if isinstance(value, int):
        return int(value)
    else:
        return int(value & sys.maxint)


def LeftShiftInt(number, step):  # 由于左移可能自动转为long型，通过这个转回来
    if isinstance((number << step), long):
        return int((number << step) - 0x200000000L)
    else:
        return int(number << step)


def getOldGTK(skey):
    a = 5381
    for i in range(0, len(skey)):
        a = a + LeftShiftInt(a, 5) + ord(skey[i])
        a = LongToInt(a)
    return a & 0x7fffffff


def getNewGTK(p_skey, skey, rv2):
    b = p_skey or skey or rv2
    a = 5381
    for i in range(0, len(b)):
        a = a + LeftShiftInt(a, 5) + ord(b[i])
        a = LongToInt(a)
    return a & 0x7fffffff


# @1h4BB3B54 804BF877775DC07D0B313E9BC345C0C10A8DC211948584EB47 1081244980
cookieStr = 'QZ_FE_WEBP_SUPPORT=0; cpu_performance_v8=52; __Q_w_s__QZN_TodoMsgCnt=1; qq_photo_key=3f5a61d2ec8b845c82cb6495b013a161; __Q_w_s_hat_seed=1; uin=o0123456789; skey=@eGUumR6t0; ptisp=cnc; qzone_check=123456789_1441331282; Loading=Yes; p_skey=dArOKuu1XrAD2eXy5WQUcc3yltbmOcl0a2R-s1SZ3ZI_; pt4_token=IrI7MG3O6TmZNggm2el42g__; qqmusic_uin=; qqmusic_key=; qqmusic_fromtag=; qzmusicplayer=qzone_player_123456789_1441331284945; pgv_info=ssid=s1620079896; p_uin=o0123456789; rv2=804BF877775DC07D0B313E9BC345C0C10A8DC211948584EB47; property20=09473DB192D9C42A2785F37178883082E9A5283893BE41ECFA493E95E6F20E27385E24C933D47B5B; '

if re.search(r'p_skey=(?P<p_skey>[^;]*)', cookieStr):
    p_skey = re.search(r'p_skey=(?P<p_skey>[^;]*)', cookieStr).group('p_skey')
else:
    p_skey = None
if re.search(r'skey=(?P<skey>[^;]*)', cookieStr):
    skey = re.search(r'skey=(?P<skey>[^;]*)', cookieStr).group('skey')
else:
    skey = None
if re.search(r'rv2=(?P<rv2>[^;]*)', cookieStr):
    rv2 = re.search(r'rv2=(?P<rv2>[^;]*)', cookieStr).group('rv2')
else:
    rv2 = None

print p_skey
print skey
print rv2
print getOldGTK(skey)
print getNewGTK(p_skey, skey, rv2)
