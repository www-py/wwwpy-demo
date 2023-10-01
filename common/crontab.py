# credits https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python

import time
from datetime import datetime, timedelta
from typing import List

from common.log_setup import getLoggerFor

logger = getLoggerFor(__file__)


class AllMatch(set):
    def __contains__(self, item): return True  # match everything

    def __str__(self) -> str: return '*'


_allMatch = AllMatch()


def _to_set(obj):
    if obj is None:
        return _allMatch
    if isinstance(obj, int):
        return {obj}  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj


class Event(object):
    def __init__(self, action, sec=None, min=None, hour=None,
                 day=None, month=None, dow=None,
                 args=(), kwargs={}, log_action_run: bool = True):
        self.log_action_run = log_action_run
        self.secs = _to_set(sec)
        self.mins = _to_set(min)
        self.hours = _to_set(hour)
        self.days = _to_set(day)
        self.months = _to_set(month)
        self.dow = _to_set(dow)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t: datetime):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.second in self.secs) and
                (t.minute in self.mins) and
                (t.hour in self.hours) and
                (t.day in self.days) and
                (t.month in self.months) and
                (t.weekday() in self.dow))

    def check(self, t: datetime):
        if not self.matchtime(t):
            return False
        if self.log_action_run:
            logger.info(f'Running job {self}')
        try:
            self.action(*self.args, **self.kwargs)
        except:
            logger.error(f'Error executing event {self}')
        return True

    def __str__(self) -> str:
        string = ' '.join(map(str, [self.secs, self.mins, self.hours, self.days, self.months, self.dow]))
        return string


class CronTab(object):
    def __init__(self, *events, log_loop: bool = False, log_executions: bool = False):
        self.log_loop = log_loop
        self.log_executions = log_executions
        self.events: List[Event] = events

    def run_thread(self, name='Cron'):
        import threading
        th = threading.Thread(target=self.run, daemon=True, name=name)
        th.start()

    def run(self):

        while True:
            t = datetime(*datetime.now().timetuple()[:6])
            t += timedelta(seconds=1)
            while datetime.now() < t:
                seconds = (t - datetime.now()).total_seconds()
                if self.log_loop:
                    logger.info(f'sleeping for {seconds}')
                time.sleep(seconds)

            if self.log_loop:
                logger.info(f'checking events count {len(self.events)}')

            executed = []
            for e in self.events:
                if e.check(t):
                    executed.append(e)

            if self.log_executions and len(executed) > 0:
                logger.info(f'executed count {len(executed)}')
                for e in executed:
                    logger.info(f'  {e}')


def main():
    action = lambda arg: print(f' {datetime.now()} happened {arg}')
    event1 = Event(action, args=(1,))
    event2 = Event(action, sec={5, 10, 30, 45, 50}, args=(2,))
    CronTab(event1, event2).run()


if __name__ == '__main__':
    main()
