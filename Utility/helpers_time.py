import datetime


def get_time() -> datetime:
    """
    teturns the current time
    [kite]
    https://www.kite.com/python/answers/how-to-calculate-a-time-difference-in-minutes-in-python#:~:text=Subtract%20one%20datetime%20object%20from,the%20time%20difference%20in%20minutes.

    :return: a datetime object containing the current time
    """
    return datetime.datetime.today()


def get_minutes(time_end: datetime, time_start: datetime) -> int:
    """
    converts 2 dates to minutes
    [kite]
    https://www.kite.com/python/answers/how-to-calculate-a-time-difference-in-minutes-in-python#:~:text=Subtract%20one%20datetime%20object%20from,the%20time%20difference%20in%20minutes.

    :param time_end: end timestamp
    :param time_start: start timestamp
    :return: minutes between them
    """
    time_delta = (time_end - time_start)
    total_seconds = time_delta.total_seconds()
    return int(total_seconds / 60)


def get_minutes_remain(minutes: int) -> int:
    """
    returns minutes remaining after converting to hours

    :param minutes: total minutes before converting to hours
    :return: minutes after converting to hours
    """
    return minutes % 60


def get_hours(minutes: int) -> int:
    """
    converts minutes to hours

    :param minutes: minutes before conversion
    :return: Hours
    """
    return int(minutes / 60)


def get_time_str(minutes: int) -> str:
    """
    teturns a printable timestamp of the difference in hours and minutes from an unconverted minutes

    :param minutes: unconverted minutes
    :return: printable string
    """

    hours = get_hours(minutes)
    minutes_remain = get_minutes_remain(minutes)
    minutes_str = ""

    if minutes_remain < 10:
        minutes_str = "0" + str(minutes_remain)
    else:
        minutes_str = str(minutes_remain)

    return str(hours) + ":" + minutes_str
