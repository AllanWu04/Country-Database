from .application_events import *
from p2app import events
from ..events import Continent


def engine_continent_search_result(view_event, connection):
    """Returns each continent found in search"""
    continent_name = view_event.name()
    continent_code = view_event.continent_code()
    if continent_name and continent_code is None:
        cursor = connection.execute('SELECT continent_id, continent_code, name '
                                    'FROM continent WHERE name = (?)', (continent_name,))
        get_continent = cursor.fetchone()
        if get_continent is None:
            return None
        create_continent = Continent(get_continent[0], get_continent[1], get_continent[2])
        return events.ContinentSearchResultEvent(create_continent)
    elif continent_code and continent_name is None:
        cursor = connection.execute('SELECT continent_id, continent_code, name '
                                    'FROM continent WHERE continent_code = (?)', (continent_code,))
        get_continent = cursor.fetchone()
        if get_continent is None:
            return None
        create_continent = Continent(get_continent[0], get_continent[1], get_continent[2])
        return events.ContinentSearchResultEvent(create_continent)
    elif continent_code and continent_name:
        cursor = connection.execute('SELECT continent_id, continent_code, name '
                                    'FROM continent WHERE continent_code = (?)'
                                    'and name = (?)', (continent_code, continent_name))
        get_continent = cursor.fetchone()
        if get_continent is None:
            return None
        create_continent = Continent(get_continent[0], get_continent[1], get_continent[2])
        return events.ContinentSearchResultEvent(create_continent)

    #cursor = connection.execute('SELECT continent_id FROM continent WHERE name = (?);', (continent_name, continent_code))
    #create_continent = Continent(cursor.fetchone(), continent_code, continent_name)
    #return events.ContinentSearchResultEvent(create_continent)

