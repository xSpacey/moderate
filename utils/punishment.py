from datetime import datetime, timedelta


def get_time():
    return datetime.now().strftime("%H:%M")


def get_date():
    return datetime.now().strftime("%d/%m/%Y")


def get_unpunish_date(duration: str):
    return 'Never' if duration == 'Never' else get_datetime() + timedelta(hours=float(duration))


def get_readable_unpunish_date(duration: float):
    return (get_datetime() + timedelta(hours=duration)).strftime('%d/%m/%Y %H:%M')


def get_datetime():
    return datetime.now()


def get_readable_datetime(dt):
    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')


def can_unpunish(time: str):
    if datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
        return True



