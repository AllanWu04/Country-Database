from .application_events import *
from p2app import events
from ..events import Region


def engine_start_region_search_event(view_event, connection):
    """Searches regions given region_code, local_code, and/or name"""
    get_region_code = view_event.region_code()
    get_local_code = view_event.local_code()
    get_name = view_event.name()
    if get_region_code:
        search_region = connection.execute('SELECT * FROM region WHERE region_code = (?)', (get_region_code,))
        get_region = search_region.fetchone()
        make_region_obj = Region(get_region[0], get_region[1], get_region[2], get_region[3], get_region[4], get_region[5], get_region[6], get_region[7])
        return events.RegionSearchResultEvent(make_region_obj)
    elif get_region_code is None and get_local_code and get_name is None:
        search_region = connection.execute('SELECT * FROM region WHERE local_code = (?)', (get_local_code,))
        get_region = search_region.fetchall()
        return get_region
    elif get_region_code is None and get_local_code is None and get_name:
        search_region = connection.execute('SELECT * FROM region WHERE name = (?)', (get_name,))
        get_region = search_region.fetchall()
        return get_region
    elif get_region_code is None and get_local_code and get_name:
        search_region = connection.execute('SELECT * FROM region WHERE local_code = (?) and name = (?)',
                                           (get_local_code, get_name))
        get_region = search_region.fetchall()
        return get_region





