import sqlite3

from .application_events import *
from p2app import events
from ..events import Region


def engine_start_region_search_event(view_event, connection):
    """Searches regions given region_code, local_code, and/or name"""
    get_region_code = view_event.region_code()
    get_local_code = view_event.local_code()
    get_name = view_event.name()
    if get_region_code:
        search_region = connection.execute('SELECT * FROM region WHERE region_code = (?);', (get_region_code,))
        get_region = search_region.fetchone()
        if get_region is None:
            return None
        make_region_obj = Region(get_region[0], get_region[1], get_region[2], get_region[3], get_region[4], get_region[5], get_region[6], get_region[7])
        return events.RegionSearchResultEvent(make_region_obj)
    elif get_region_code is None and get_local_code and get_name is None:
        search_region = connection.execute('SELECT * FROM region WHERE local_code = (?);', (get_local_code,))
        get_region = search_region.fetchall()
        if get_region is None:
            return None
        return get_region
    elif get_region_code is None and get_local_code is None and get_name:
        search_region = connection.execute('SELECT * FROM region WHERE name = (?);', (get_name,))
        get_region = search_region.fetchall()
        if get_region is None:
            return None
        return get_region
    elif get_region_code is None and get_local_code and get_name:
        search_region = connection.execute('SELECT * FROM region WHERE local_code = (?) and name = (?);',
                                           (get_local_code, get_name))
        get_region = search_region.fetchall()
        if get_region is None:
            return None
        return get_region


def engine_region_loaded_event(view_event, connection):
    """Loads information about a selected region"""
    get_region_id = view_event.region_id()
    find_region = connection.execute('SELECT * FROM region WHERE region_id = (?);', (get_region_id,))
    get_info = find_region.fetchone()
    make_region_obj = Region(get_info[0], get_info[1], get_info[2], get_info[3], get_info[4], get_info[5], get_info[6], get_info[7])
    return events.RegionLoadedEvent(make_region_obj)


def engine_save_new_region_event(view_event, connection):
    """Creates a new region for the database"""
    get_new_region = view_event.region()
    check_if_region_exist = connection.execute('SELECT * FROM region WHERE region_code = (?);', (get_new_region[1],))
    get_region_exist = check_if_region_exist.fetchone()
    if get_region_exist is None and get_new_region[1] != '' and get_new_region[2] != '' and get_new_region[3] != '' and get_new_region[4] != '' and get_new_region[5] != '':
        connection.execute('INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) '
                            'VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
                            (get_new_region[0], get_new_region[1], get_new_region[2], get_new_region[3],
                            get_new_region[4], get_new_region[5], get_new_region[6], get_new_region[7]))
        connection.commit()
        return events.RegionSavedEvent(get_new_region)
    else:
        if get_region_exist:
            return events.SaveRegionFailedEvent('Sorry, region code exists already!')
        else:
            return events.SaveRegionFailedEvent('Sorry, there are required values left empty!')


def engine_save_edited_region(view_event, connection):
    """Edits any selected region from the search"""
    get_edited_region_info = view_event.region()
    check_if_valid_region_code = connection.execute('SELECT * '
                                                    'FROM region '
                                                    'WHERE region_code = (?)',
                                                    (get_edited_region_info[1],))
    check_if_exist = check_if_valid_region_code.fetchone()
    if get_edited_region_info[1] == '' or get_edited_region_info[2] == '' or get_edited_region_info[3] == '' or get_edited_region_info[4] == '' or get_edited_region_info[5] == '':
        return events.SaveRegionFailedEvent('Sorry, there are required values left empty!')
    if check_if_exist is None or check_if_exist[1] == get_edited_region_info[1]:
        connection.execute('UPDATE region '
                            'SET region_code = (?), local_code = (?), name = (?), continent_id = (?), country_id = (?), wikipedia_link = (?), keywords = (?) '
                            'WHERE region_id = (?);', (get_edited_region_info[1], get_edited_region_info[2],
                                                        get_edited_region_info[3], get_edited_region_info[4],
                                                        get_edited_region_info[5], get_edited_region_info[6],
                                                        get_edited_region_info[7], get_edited_region_info[0]))
        connection.commit()
        return events.RegionSavedEvent(get_edited_region_info)
    else:
        return events.SaveRegionFailedEvent('Sorry, this region_code already exists!')



