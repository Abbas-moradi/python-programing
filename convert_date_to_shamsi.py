def future_date(month=0, day=0) -> datetime:
    from datetime import datetime
    import jdatetime

    now = datetime.now()
    future = now.timestamp() + (((month * 30.44) + day) * 86286.47)
    j = jdatetime.datetime.fromtimestamp(future)
    return j


print(future_date(0, 0))