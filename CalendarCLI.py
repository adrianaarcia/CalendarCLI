from Calendar import Calendar
import sys
from tabulate import tabulate

import Calendar_exceptions as exc

from datetime import datetime
import os
import logging
logging.basicConfig(filename="calendar.log", level=logging.DEBUG)

class CalendarCLI():
    def __init__(self):
        self.calendar = Calendar()

        self.choices = {
            "view": self.view,
            "create": self.create,
            "contacts": self.contacts,
            "delete": self.delete,
            "load": self.load,
            "save": self.save,
            "quit": self.quit
        }

    def _print_event(self, event):
        print(tabulate([[str(event)]], tablefmt='grid'))

    def display_menu(self):
        print("Enter command \nview, contacts, create, delete, load, save, quit")

    def run(self):
        """Display the menu and respond to choices."""
        try:
            while True:
                self.display_menu()
                choice = input(">")
                action = self.choices.get(choice)
                if action:
                    action()
                else:
                    print("{0} is not a valid choice".format(choice))
        except Exception as err:
            print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
            logging.exception(err)

    def view(self):
        try:
            view_type = input('"all" or "<contact name>"\n>')
            if view_type == "all":
                events = self.calendar.show_events()
            else:
                events = self.calendar.show_events_by_contact(view_type)
            for event in events:
                self._print_event(event)
        except exc.EmptyCalendarError:
            print("No meetings to show")
            return
    
    def contacts(self):
        for contact in self.calendar.show_contacts():
            print(contact)

    def create(self):
        try:
            title = input("Title?\n>")
            date = input("Date? (YYYY-MM-DD)\n>")
            start = input("Start time? (HH:MM in 24-hour format)\n>")
            end = input("End time? (HH:MM in 24-hour format)\n>")
            is_meeting = input('Invite others? "yes" or "no"\n>')
            if is_meeting == "yes":
                invites = []
                invite = input('"<Contact name>" or "done"\n>')
                while (invite != "done"):
                    invites.append(invite)
                    invite = input('"<Contact name>" or "done"\n>')
                self.calendar.add_event(
                    title, date, start, end, *invites)
            else:
                self.calendar.add_event(title, date, start, end)

        except ValueError as e:
            print("Cannot create this event. " + str(e))
            return
        except exc.InvalidDateError as e:
            print("Cannot create an event with a date of {}. Try again with this date format YYYY-MM-DD.".format(e.inp))
            return
        except exc.InvalidTimeError as e:
            print("Cannot create an event with a time of {}. Try again with this time format HH:MM.".format(e.inp))
            return
            #print(f"Cannot create an event with a {e.type} of {e.inp}. Try again with this {e.type} format {e.format}")
        except exc.CalendarConflictError as e:
            print("Cannot add this event because it conflicts with this event...")
            self._print_event(e)
            return

    def delete(self):
        try:
            index = input(
            "Which event?\nEnter an index 1..n to identify the event from the sorted list\n>")
            self.calendar.delete(int(index) - 1)
        except IndexError:
            print("No such event.")
            return


    def load(self):
        self.calendar = Calendar()
        with open("save.csv", "r") as f:
            for line in f.readlines():
                fields = line.strip().split(",")
                self.calendar.add_event(*fields)
        logging.debug("{}, Loaded calendar from {}/save.csv".format(datetime.now().isoformat(), os.getcwd()))


    def save(self):
        with open("save.csv", "w") as f:
            for e in self.calendar.show_events():
                f.write(repr(e) + "\n")
        logging.debug("{}, Saved calendar to {}/save.csv".format(datetime.now().isoformat(), os.getcwd()))

    def quit(self):
        sys.exit(0)


if __name__ == "__main__":
    CalendarCLI().run()
