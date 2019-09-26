import os

def check_time(time):
    separate_time = time.split(':')
    try:
        hours = int(separate_time[0])
        minutes = int(separate_time[1])
    except ValueError:
        print("Format entered is not valid timestamp.")
    return hours, minutes 