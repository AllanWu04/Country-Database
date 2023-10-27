from .application_events import *
from p2app import events
from ..events import Continent


def engine_continent_search_result(view_event, connection):
    """Returns each continent found in search"""
    continent_name = view_event.name()
    continent_code = view_event.continent_code()
    cursor = connection.execute('SELECT continent_id FROM continent WHERE name = (?) and continent_code = (?) ;', (continent_name, continent_code))
    create_continent = Continent(cursor.fetchone(), continent_code, continent_name)
    return events.ContinentSearchResultEvent(create_continent)

