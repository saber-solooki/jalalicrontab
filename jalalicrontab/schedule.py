from bisect import bisect, bisect_left

from celery.schedules import crontab
from celery.utils.collections import AttributeDict
from celery.utils.time import ffwd

from jalalicrontab.utils.time import jalalidatetime


class JalaliCrontab(crontab):
    datetime_cls = jalalidatetime

    def now(self):
        return self.datetime_cls.now()

    def _delta_to_next(self, last_run_at, next_hour, next_minute):
        """Find next delta. Actually this function is just like the parent class,
        otherwise :class:`~datetime.datetime` is replaced with
        :class:`~jdatetime.datetime`

        Takes a :class:`~datetime.datetime` of last run, next minute and hour,
        and returns a :class:`~celery.utils.time.ffwd` for the next
        scheduled day and time.

        Only called when ``day_of_month`` and/or ``month_of_year``
        cronspec is specified to further limit scheduled task execution.
        """
        datedata = AttributeDict(year=last_run_at.year)
        days_of_month = sorted(self.day_of_month)
        months_of_year = sorted(self.month_of_year)

        def day_out_of_range(year, month, day):
            try:
                self.datetime_cls(year=year, month=month, day=day)
            except ValueError:
                return True
            return False

        def is_before_last_run(year, month, day):
            return self.maybe_make_aware(
                self.datetime_cls(year, month, day)) < last_run_at

        def roll_over():
            for _ in range(2000):
                flag = (datedata.dom == len(days_of_month) or
                        day_out_of_range(datedata.year,
                                         months_of_year[datedata.moy],
                                         days_of_month[datedata.dom]) or
                        (is_before_last_run(datedata.year,
                                            months_of_year[datedata.moy],
                                            days_of_month[datedata.dom])))

                if flag:
                    datedata.dom = 0
                    datedata.moy += 1
                    if datedata.moy == len(months_of_year):
                        datedata.moy = 0
                        datedata.year += 1
                else:
                    break
            else:
                # Tried 2000 times, we're most likely in an infinite loop
                raise RuntimeError('unable to rollover, '
                                   'time specification is probably invalid')

        if last_run_at.month in self.month_of_year:
            datedata.dom = bisect(days_of_month, last_run_at.day)
            datedata.moy = bisect_left(months_of_year, last_run_at.month)
        else:
            datedata.dom = 0
            datedata.moy = bisect(months_of_year, last_run_at.month)
            if datedata.moy == len(months_of_year):
                datedata.moy = 0
        roll_over()

        while 1:
            th = self.datetime_cls(year=datedata.year,
                                   month=months_of_year[datedata.moy],
                                   day=days_of_month[datedata.dom])
            if th.isoweekday() % 7 in self.day_of_week:
                break
            datedata.dom += 1
            roll_over()

        return ffwd(year=datedata.year,
                    month=months_of_year[datedata.moy],
                    day=days_of_month[datedata.dom],
                    hour=next_hour,
                    minute=next_minute,
                    second=0,
                    microsecond=0)

    def remaining_estimate(self, last_run_at, ffwd=ffwd):
        if type(last_run_at) != self.datetime_cls:
            last_run_at = self.datetime_cls.fromgregorian(datetime=last_run_at)
        return super().remaining_estimate(last_run_at, ffwd)

    def __reduce__(self):
        return (self.__class__, (self._orig_minute,
                                 self._orig_hour,
                                 self._orig_day_of_week,
                                 self._orig_day_of_month,
                                 self._orig_month_of_year), self._orig_kwargs)
