from datetime import datetime
from dateutil.relativedelta import relativedelta

def time_ago(lastUpdatedNovels):
    for index, novel in enumerate(lastUpdatedNovels):
        now = datetime.now()
        diff = relativedelta(now, novel['date_edited'])
        
        if diff.years > 0:
            val = f"{diff.years} year{'s' if diff.years > 1 else ''} ago"
        elif diff.months > 0:
            val = f"{diff.months} month{'s' if diff.months > 1 else ''} ago"
        elif diff.days > 0:
            val = f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.hours > 0:
            val = f"{diff.hours} hour{'s' if diff.hours > 1 else ''} ago"
        elif diff.minutes > 0:
            val = f"{diff.minutes} minute{'s' if diff.minutes > 1 else ''} ago"
        else:
            val = f"{diff.seconds} second{'s' if diff.seconds > 1 else ''} ago"
        
        lastUpdatedNovels[index]['date_edited'] = val

    return lastUpdatedNovels
