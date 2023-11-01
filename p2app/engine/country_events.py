import sqlite3

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
                                    'WHERE name = (?);', (get_country_name,))
        get_info = cursor.fetchall()
        if get_info is None:
            return None
        return get_info
    elif get_country_name is None and get_country_code:
        cursor = connection.execute('SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords '
                                    'FROM country '
                                    'WHERE country_code = (?);', (get_country_code,))
        get_info = cursor.fetchone()
        if get_info is None:
            return None
        create_country = Country(get_info[0], get_info[1], get_info[2], get_info[3], get_info[4], get_info[5])
        return events.CountrySearchResultEvent(create_country)
    elif get_country_name and get_country_code:
        cursor = connection.execute('SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords '
                                    'FROM country '
                                    'WHERE country_code = (?) and name = (?);', (get_country_code, get_country_name))
        get_info = cursor.fetchone()
        if get_info is None:
            return None
        create_country = Country(get_info[0], get_info[1], get_info[2], get_info[3], get_info[4], get_info[5])
        return events.CountrySearchResultEvent(create_country)


def engine_loaded_country_event(view_event, connection):
    """Return the information of a country when edited"""
    get_country_id = view_event.country_id()
    find_country = connection.execute('SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords '
                                        'FROM country WHERE country_id = (?);', (get_country_id,))
    get_country = find_country.fetchone()
    make_country = Country(get_country[0], get_country[1], get_country[2], get_country[3], get_country[4], get_country[5])
    return events.CountryLoadedEvent(make_country)


def engine_save_new_country(view_event, connection):
    """Creates a new country with given information from view_event"""
    get_view_country = view_event.country()
    check_exist_country = connection.execute('SELECT * FROM country '
                                             'WHERE country_code = (?);', (get_view_country[1],))
    attempt_get_country = check_exist_country.fetchone()
    if attempt_get_country is None and get_view_country[2] != '' and get_view_country[3] != '' and get_view_country[4] != '':
        try:
            connection.execute('INSERT INTO country '
                            '(country_id, country_code, name, continent_id, wikipedia_link, keywords) '
                           'VALUES (?, ?, ?, ?, ?, ?);',
                           (get_view_country[0], get_view_country[1], get_view_country[2],
                            get_view_country[3], get_view_country[4], get_view_country[5]))
            return events.CountrySavedEvent(get_view_country)
        except sqlite3.IntegrityError:
            return events.SaveCountryFailedEvent("Sorry, there are missing/invalid values for the country.")
    else:
        if attempt_get_country:
            return events.SaveCountryFailedEvent("Sorry, the country code is already taken!")
        else:
            return events.SaveCountryFailedEvent("Sorry, there are required values left empty.")


def engine_save_edited_country(view_event, connection):
    """Edits a country that exists in the database"""
    update_country = view_event.country()
    if update_country[1] == '' or update_country[2] == '' or update_country[3] == 0 or update_country[4] == '':
        return events.SaveCountryFailedEvent("Sorry, there are required values left empty!")
    try:
        change_country = connection.execute('UPDATE country '
                                            'SET country_code = (?), name = (?), continent_id = (?), wikipedia_link = (?), keywords = (?) '
                                            'WHERE country_id = (?);',
                                            (update_country[1], update_country[2], update_country[3], update_country[4], update_country[5], update_country[0]))
        return events.CountrySavedEvent(update_country)
    except sqlite3.IntegrityError:
        return events.SaveCountryFailedEvent("Sorry, the country code already exists in the database or continent_id is invalid!")
