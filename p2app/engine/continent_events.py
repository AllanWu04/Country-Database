import sqlite3

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
        get_continent = cursor.fetchall()
        if get_continent is None:
            return None
        return get_continent
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
    """Loads information about continent when edited"""
    continent_id = view_event.continent_id()
    cursor = connection.execute('SELECT continent_id, continent_code, name '
                                'FROM continent WHERE continent_id = (?);', (continent_id,))
    get_info = cursor.fetchone()
    create_continent = Continent(get_info[0], get_info[1], get_info[2])
    return events.ContinentLoadedEvent(create_continent)


def engine_save_new_continent(view_event, connection):
    """Creates a new continent with name and continent code"""
    get_continent_from_view = view_event.continent()
    continent_code_of_new_continent = get_continent_from_view.continent_code
    cursor = connection.execute('SELECT * '
                                'FROM continent WHERE continent_code = (?);',
                                (continent_code_of_new_continent,))
    check_if_exists = cursor.fetchone()
    if check_if_exists is None and get_continent_from_view.name != '' and continent_code_of_new_continent != '':
        connection.execute('INSERT INTO continent (continent_id, continent_code, name) '
                           'VALUES (?, ?, ?);',
                           (get_continent_from_view[0], get_continent_from_view[1], get_continent_from_view[2]))
        return events.ContinentSavedEvent(get_continent_from_view)
    else:
        return events.SaveContinentFailedEvent("This Continent is Invalid")


def engine_save_edited_continent(view_event, connection):
    """Edits a continent by changing its name and/or continent code"""
    get_view_continent = view_event.continent()
    view_continent_id = get_view_continent.continent_id
    view_continent_code = get_view_continent.continent_code
    view_continent_name = get_view_continent.name
    if view_continent_code == '' or view_continent_name == '':
        return events.SaveContinentFailedEvent("This Continent is Invalid!")
    try:
        cursor = connection.execute('UPDATE continent SET continent_code = (?), name = (?) '
                                    'WHERE continent_id = (?);',
                                    (view_continent_code, view_continent_name, view_continent_id))
        return events.ContinentSavedEvent(get_view_continent)
    except sqlite3.IntegrityError:
        return events.SaveContinentFailedEvent("This Continent is Invalid!")

