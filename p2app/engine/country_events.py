
from .application_events import *
from p2app import events
from ..events import Country


def engine_start_country_search_event(view_event, connection):
    """Searches for countries given their country code and their name"""
    get_country_code = view_event.country_code()
    get_country_name = view_event.name()
    if get_country_name and get_country_code is None:
        cursor = connection.execute('SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords '
                                    'FROM country '
                                    'WHERE name = (?)', (get_country_name,))
        get_info = cursor.fetchall()
        if get_info is None:
            return None
        return get_info
    elif get_country_name is None and get_country_code:
        cursor = connection.execute('SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords '
                                    'FROM country '
                                    'WHERE country_code = (?)', (get_country_code,))
        get_info = cursor.fetchone()
        if get_info is None:
            return None
        create_country = Country(get_info[0], get_info[1], get_info[2], get_info[3], get_info[4], get_info[5])
        return events.CountrySearchResultEvent(create_country)
    elif get_country_name and get_country_code:
        cursor = connection.execute('SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords '
                                    'FROM country '
                                    'WHERE country_code = (?) and name = (?)', (get_country_code, get_country_name))
        get_info = cursor.fetchone()
        if get_info is None:
            return None
        create_country = Country(get_info[0], get_info[1], get_info[2], get_info[3], get_info[4], get_info[5])
        return events.CountrySearchResultEvent(create_country)
