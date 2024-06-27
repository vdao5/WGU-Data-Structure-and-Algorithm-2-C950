from datetime import datetime, timedelta

# dtime is a timedelta object with a formated string / int constructor
# and a int() method to return the time in a 4 digit integer format
# e.g. dtime('1234') or dt(1234) -> 12:34:00
class dtime(timedelta):
    def __new__(cls, input: str | int = None, **kargs):
        if input is None:
            return super().__new__(cls, **kargs)
        
        dt = datetime.strptime(str(input), '%H%M')
        return super().__new__(cls, hours=dt.hour, minutes=dt.minute)
    
    def __int__(self):
        return 100 * int(self.seconds / 3600) + int(self.seconds % 3600 / 60)