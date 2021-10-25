
class EmptyCalendarError(Exception):
    def __init__(self):
        pass

class InvalidDateError(Exception):
    def __init__(self, input):
        self.inp = input
    
class InvalidTimeError(Exception):
    def __init__(self, input):
        self.inp = input

class CalendarConflictError(Exception):
    def __init__(self, ev):
        self.inv_ev = ev