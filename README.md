# CalendarCLI
A simple Calendar application with a command line interface. 

## Overview
This application allows you to 
* create/delete events, 
* add contacts to meetings,
* view all contacts,
* view all meetings in the schedule,
* view all meetings in the schedule attended by a specific contact,
* and load/save in a file.

Main file 
* CalendarCLI.py: Driver for the CLI 
Classes 
* Calendar: Top-level container/management class 
* Event: Base class for calendar events 
* Meeting: Class for events that also include invited contacts 
* Contact: Class for people invited to meetings 

## Known Bugs and Possible Improvements
* validate input
* redundancy in adding contact to set of contacts
* Add show events method for contacts
