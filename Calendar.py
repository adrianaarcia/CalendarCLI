from Event import Event
from Contact import Contact
from Meeting import Meeting
import Calendar_exceptions as exc

from datetime import datetime
import os
import logging
logging.basicConfig(filename="calendar.log", level=logging.DEBUG)

class Calendar:
    def __init__(self):
        self._contacts = set([])
        self._events = []

    def add_contact(self, contact):
        if contact not in self._contacts:
            self._contacts.add(contact)
            logging.debug("{}, Created contact: {}".format(datetime.now().isoformat(), repr(contact)))

    def add_event(self, title, day, start_time, end_time, *args):
        if len(args) > 0:
            new_event = Meeting(title, day, start_time, end_time)
        else:
            new_event = Event(title, day, start_time, end_time)
        for event in self._events:
            if new_event.collides_with(event):
                raise exc.CalendarConflictError(event)
        for invite in args:
            c = Contact(invite)
            new_event.add_participant(c)
            self.add_contact(c)
        self._events.append(new_event)
        logging.debug("{}, Created event: {}".format(datetime.now().isoformat(), repr(new_event)))

    def show_contacts(self):
        return sorted(self._contacts)

    def show_events(self, events=None):
        if events is None:
            events = self._events
        if not events:
            raise exc.EmptyCalendarError
        return sorted(events)

    def show_events_by_contact(self, name):
        c = Contact(name)

        meetings = [event for event in self._events if event.match(c)]
        return self.show_events(events=meetings)

    def delete(self, index):
        event = sorted(self._events)[index]
        self._events.remove(event)
        logging.debug("{}, Deleted event: {}".format(datetime.now().isoformat(), repr(event)))
