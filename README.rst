JalaliCrontab
=============

.. image:: https://img.shields.io/pypi/v/celery-jalalicrontab.svg
   :target: https://pypi.python.org/pypi/celery-jalalicrontab
   :alt: PyPI

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black

`JalaliCrontab <https://github.com/saber-solooki/jalalicrontab>`_ is a
`Celery schedule <https://docs.celeryproject.org/en/stable/reference/celery.schedules.html>`_
that works with `Jalali Calendar <https://en.wikipedia.org/wiki/Jalali_calendar>`_.

Getting Started
---------------

Install with pip:

.. code-block:: console

    pip install celery-jalalicrontab

You can use JalaliCrontab just like celery crontab. In the example bellow,
task will be run every minutes in "30" of "dey" month:

.. code-block:: python

    @app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        sender.add_periodic_task(
            JalaliCrontab(day_of_month=30, month_of_year=10),
            test.s('Happy my birthday!'),
        )

And also you can use it alongside RedisBeater by extending `JalaliCrontab` and
`jalalidatetime` then define `encode_beater` method for them:

.. code-block:: python

    class Myjalalidatetime(jalalidatetime):
        def encode_beater(self):
            if self.tzinfo is None:
                timezone = 'UTC'
            elif self.tzinfo.zone is None:
                timezone = self.tzinfo.utcoffset(None).total_seconds()
            else:
                timezone = self.tzinfo.zone

            datetime_obj = self.togregorian()
            return {
                'year': datetime_obj.year,
                'month': datetime_obj.month,
                'day': datetime_obj.day,
                'hour': datetime_obj.hour,
                'minute': datetime_obj.minute,
                'second': datetime_obj.second,
                'microsecond': datetime_obj.microsecond,
                'timezone': timezone,
            }

    class MyJalaliCrontab(JalaliCrontab):
        def encode_beater(self):
            return {
                'minute': self._orig_minute,
                'hour': self._orig_hour,
                'day_of_week': self._orig_day_of_week,
                'day_of_month': self._orig_day_of_month,
                'month_of_year': self._orig_month_of_year,
            }

Development
-----------
JalaliCrontab is available on `GitHub <https://github.com/saber-solooki/jalalicrontab>`_

Once you have the source you can run the tests with the following commands::

    pip install -r requirements.dev.txt
    py.test tests

