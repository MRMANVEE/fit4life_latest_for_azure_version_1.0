from datetime import datetime




def changeDateFormatOnly(FinalDate):
    dateModification = FinalDate.split('-')
    return f"{dateModification[2]}/{dateModification[1]}/{dateModification[0]}"

def changingTimeFormat24T12(time):
    Tsplitedtime = time.split(':')
    return (datetime.strptime(f"{Tsplitedtime[0]}:{Tsplitedtime[1]}", "%H:%M").time()).strftime("%I:%M %p")

#ss
def changeTimeFormat(date_time):
    date_time_split = date_time.split()
    date_split = date_time_split[0].split('-')
    edited_format_date = date_split[2] + '/' + date_split[1] + '/' + date_split[0]
    final = edited_format_date + '  ' + changingTimeFormat24T12(date_time_split[1])
    return final


def change_date_format_ical(data):
    st_date = str(data)
    date_splite = st_date.split()
    data_sp = date_splite[0].split('-')
    time_sp = date_splite[1].split(':')
    total_date = data_sp[0] + data_sp[1]+data_sp[2]
    total_time  = time_sp[0] + time_sp[1] + time_sp[2]
    return total_date+'T'+total_time