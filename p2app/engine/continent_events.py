from .application_events import *
from p2app import events
from ..events import Continent


def engine_continent_search_result(view_event, connection):
    """Returns each continent found in search"""
    continent_name = view_event.name()
    continent_code = view_event.continent_code()
    if continent_name and continent_code is None:
        cursor = connection.execute('SELECT continent_id, continent_code, name '
                                    'FROM continent WHERE name = (?);', (continent_name,))
        get_continent = cursor.fetchone()
        if get_continent is None:
            return None
        create_continent = Continent(get_continent[0], get_continent[1], get_continent[2])
        return events.ContinentSearchResultEvent(create_continent)
    elif continent_code and continent_name is None:
        cursor = connection.execute('SELECT continent_id, continent_code, name '
                                    'FROM continent WHERE continent_code = (?);', (continent_code,))
        get_continent = cursor.fetchone()
        if get_continent is None:
            return None
        create_continent = Continent(get_continent[0], get_continent[1], get_continent[2])
        return events.ContinentSearchResultEvent(create_continent)
    elif continent_code and continent_name:
        cursor = connection.execute('SELECT continent_id, continent_code, name '
                                    'FROM continent WHERE continent_code = (?)'
                                    'and name = (?);', (continent_code, continent_name))
        get_continent = cursor.fetchone()
        if get_continent is None:
            return None
        create_continent = Continent(get_continent[0], get_continent[1], get_continent[2])
        return events.ContinentSearchResultEvent(create_continent)


def engine_continent_loaded(view_event, connection):
    continent_id = view_event.continent_id()
    cursor = connection.execute('SELECT continent_id, continent_code, name '
                                'FROM continent WHERE continent_id = (?);', (continent_id,))
    get_info = cursor.fetchone()
    create_continent = Continent(get_info[0], get_info[1], get_info[2])
    return events.ContinentLoadedEvent(create_continent)


def engine_save_new_continent(view_event, connection):
    get_continent_from_view = view_event.continent()
    name_of_new_continent = get_continent_from_view.name
    continent_code_of_new_continent = get_continent_from_view.continent_code
    cursor = connection.execute('SELECT continent_id, continent_code, name '
                                'FROM continent WHERE name = (?) or continent_code = (?);',
                                (name_of_new_continent, continent_code_of_new_continent))
    check_if_exists = cursor.fetchone()
    if check_if_exists is None:
        connection.execute('INSERT INTO continent (continent_id, continent_code, name) '
                           'VALUES (?, ?, ?);', (get_continent_from_view[0], get_continent_from_view[1], get_continent_from_view[2]))
        return events.ContinentSavedEvent(get_continent_from_view)
    else:
        return events.SaveContinentFailedEvent("This Continent Already Exists!")

