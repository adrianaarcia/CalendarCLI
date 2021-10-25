from datetime import date, time

from Comparable import ComparableMixin
import Calendar_exceptions as exc

class Event(ComparableMixin):

    def __init__(self, title, day, start_time, end_time):
        self._validate_title(title)
        try:

            self._date = date.fromisoformat(day)
        except ValueError:
            raise exc.InvalidDateError(day)
        
        try:
            self._start_time = time.fromisoformat(start_time)
        except ValueError:
            raise exc.InvalidTimeError(start_time)
        
        try:
            self._end_time = time.fromisoformat(end_time)
        except ValueError:
            raise exc.InvalidTimeError(end_time)

    def __str__(self):
        return "{}\nDate: {}\nTime: {} - {}\n".format(self._title, self._date.isoformat(), self._format_time(self._start_time), self._format_time(self._end_time))

    def __repr__(self):
        return ",".join([self._title, self._date.isoformat(), self._format_time(self._start_time), self._format_time(self._end_time)])

    def __lt__(self, other):
        if self._date == other._date:
            return self._start_time < other._start_time
        else:
            return self._date < other._date

    def __eq__(self, other):
        return self._title == other._title and self._date == other._date

    def collides_with(self, other):
        if self._date != other._date:
            return False
        if other._start_time >= self._start_time and other._start_time < self._end_time:
            return True
        if self._start_time >= other._start_time and self._start_time < other._end_time:
            return True
        return False

    def duration(self):
        return self._end_time - self._start_time

    def match(self, criteria):
        "Not implemented for this class. Always returns False."
        return False

    def _format_time(self, t):
        return t.strftime('%H:%M')

    def _validate_title(self, title):
        #strp = title.strip()
        if not title or title.isspace():
            raise ValueError("The title cannot be blank.")
        if ',' in title:
            raise ValueError("The title must not contain commas.")
        #elif not strp or strp.isspace():
        #elif not title or not strp or title.isspace() or strp.isspace():
           #raise ValueError("The title cannot be blank.")
        else:
            self._title = title


