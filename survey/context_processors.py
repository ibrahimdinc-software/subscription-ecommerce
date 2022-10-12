from random import randint
from datetime import datetime, timedelta
from django.core.cache import cache


def viewer(request):
    # Check the IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    # Get the list of the latest online users
    online = cache.get('online_now')
    time = cache.get('last_time')
    # Check the active IP addresses
    #r = cache.get('r')
    """
    if not time:
        time = datetime.now()
        cache.set('r', randint(7, 15))
    elif time + timedelta(minutes=15) < datetime.now():
        cache.set('r', randint(7, 15))
        time = datetime.now()
        print("work")
    """

    if online:
        online = [ip for ip in online if cache.get(ip)]
    else:
        online = []
    # Add the new IP to cache
    cache.set(user_ip, user_ip, 600)
    # Add the new IP to list if doesn't exist
    if user_ip not in online:
        online.append(user_ip)
    # Set the new online list
    cache.set('online_now', online)
    #cache.set('last_time', time)
    # Add the number of online users to request
    return {"online": 5 + len(online)}
