from functools import wraps

import datetime
import jdatetime


_tzinfo_class = datetime.tzinfo


def jalali_convertor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_result = func(*args, **kwargs)

        if type(func_result) == jdatetime.datetime:
            return jalalidatetime(func_result.year, func_result.month, func_result.day,
                                  func_result.hour, func_result.minute,
                                  func_result.second, func_result.microsecond,
                                  func_result.tzinfo, locale=func_result.locale)
        else:
            return func_result

    return wrapper


class jalalidatetime(jdatetime.datetime):
    def __init__(self, year, month, day, hour=0, minute=0, second=0,
                 microsecond=0, tzinfo=None, fold=0, **kwargs):
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._hashcode = -1
        self._fold = fold

        super().__init__(year, month, day, hour=hour, minute=minute, second=second,
                         microsecond=microsecond, tzinfo=tzinfo, fold=fold, **kwargs)

    @property
    def __class__(self):
        return datetime.datetime

    @staticmethod
    @jalali_convertor
    def fromgregorian(**kw):
        return jdatetime.datetime.fromgregorian(**kw)

    @jalali_convertor
    def replace(self, year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, tzinfo=True):
        return super(jalalidatetime, self).replace(year, month, day, hour, minute,
                                                     second, microsecond, tzinfo)

    @jalali_convertor
    def astimezone(self, tz):
        return super(jalalidatetime, self).astimezone(tz)

    @staticmethod
    @jalali_convertor
    def today():
        return jdatetime.datetime.now()

    @staticmethod
    @jalali_convertor
    def now(tz=None):
        return jdatetime.datetime.now()

    @staticmethod
    @jalali_convertor
    def utcnow():
        return jdatetime.datetime.utcnow()

    @staticmethod
    @jalali_convertor
    def fromtimestamp(timestamp, tz=None):
        return jdatetime.datetime.fromtimestamp(timestamp, tz)

    @staticmethod
    @jalali_convertor
    def utcfromtimestamp(timestamp):
        return jdatetime.datetime.utcfromtimestamp(timestamp)

    @staticmethod
    @jalali_convertor
    def combine(d=None, t=None, **kw):
        return jdatetime.datetime.combine(d, t, **kw)

    @staticmethod
    @jalali_convertor
    def fromordinal(ordinal):
        return jdatetime.datetime.fromordinal(ordinal)

    @staticmethod
    @jalali_convertor
    def strptime(date_string, format):
        return jdatetime.datetime.strptime(date_string, format)

    def __add__(self, timedelta):
        if isinstance(timedelta, datetime.timedelta):
            return jalalidatetime.fromgregorian(
                datetime=self.togregorian() + timedelta, locale=self.locale)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        """x.__sub__(y) <==> x-y"""

        if isinstance(other, datetime.timedelta):
            return jalalidatetime.fromgregorian(datetime=self.togregorian() - other,
                                                locale=self.locale)
        if type(other) == datetime.datetime:
            return self.togregorian() - other
        if type(other) == jdatetime.datetime or type(other) == jalalidatetime:
            return self.togregorian() - other.togregorian()
        return NotImplemented

    __rsub__ = __sub__

    # Pickle support.

    def _getstate(self, protocol=3):
        yhi, ylo = divmod(self._year, 256)
        us2, us3 = divmod(self._microsecond, 256)
        us1, us2 = divmod(us2, 256)
        m = self._month
        if self._fold and protocol > 3:
            m += 128
        basestate = bytes([yhi, ylo, m, self._day,
                           self._hour, self._minute, self._second,
                           us1, us2, us3])
        if self._tzinfo is None:
            return basestate,
        else:
            return basestate, self._tzinfo

    def __setstate(self, string, tzinfo):
        if tzinfo is not None and not isinstance(tzinfo, _tzinfo_class):
            raise TypeError("bad tzinfo state arg")
        (yhi, ylo, m, self._day, self._hour,
         self._minute, self._second, us1, us2, us3) = string
        if m > 127:
            self._fold = 1
            self._month = m - 128
        else:
            self._fold = 0
            self._month = m
        self._year = yhi * 256 + ylo
        self._microsecond = (((us1 << 8) | us2) << 8) | us3
        self._tzinfo = tzinfo

    def __reduce_ex__(self, protocol):
        return self.__class__, self._getstate(protocol)

    def __reduce__(self):
        return self.__reduce_ex__(2)
