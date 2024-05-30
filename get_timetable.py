from timetable import getTimetableData

timetable = getTimetableData(6847)
with open('data/timetable.json', 'w') as tf:
    tf.write(timetable)