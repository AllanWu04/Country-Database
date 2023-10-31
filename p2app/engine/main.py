# p2app/engine/main.py
#
# ICS 33 Fall 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

from p2app import events
from .application_events import *
from .continent_events import *
from .country_events import *
from .region_events import *
from p2app import events

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.create_connection = None

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if isinstance(event, events.OpenDatabaseEvent):
            yield engine_open_event(event, self)
        elif isinstance(event, events.CloseDatabaseEvent):
            yield engine_close_event()
        elif isinstance(event, events.QuitInitiatedEvent):
            yield engine_end_application()
        elif isinstance(event, events.StartContinentSearchEvent):
            if event.continent_code() is None:
                continent_results = engine_continent_search_result(event, self.create_connection)
                for i in continent_results:
                    make_continent = Continent(i[0], i[1], i[2])
                    yield events.ContinentSearchResultEvent(make_continent)
            yield engine_continent_search_result(event, self.create_connection)
        elif isinstance(event, events.LoadContinentEvent):
            yield engine_continent_loaded(event, self.create_connection)
        elif isinstance(event, events.SaveNewContinentEvent):
            yield engine_save_new_continent(event, self.create_connection)
        elif isinstance(event, events.SaveContinentEvent):
            yield engine_save_edited_continent(event, self.create_connection)
        elif isinstance(event, events.StartCountrySearchEvent):
            if event.country_code() is None:
                country_results = engine_start_country_search_event(event, self.create_connection)
                for i in country_results:
                    make_country_obj = Country(i[0], i[1], i[2], i[3], i[4], i[5])
                    yield events.CountrySearchResultEvent(make_country_obj)
            yield engine_start_country_search_event(event, self.create_connection)
        elif isinstance(event, events.LoadCountryEvent):
            yield engine_loaded_country_event(event, self.create_connection)
        elif isinstance(event, events.SaveNewCountryEvent):
            yield engine_save_new_country(event, self.create_connection)
        elif isinstance(event, events.SaveCountryEvent):
            yield engine_save_edited_country(event, self.create_connection)
        elif isinstance(event, events.StartRegionSearchEvent):
            if event.region_code() is None:
                all_region_results = engine_start_region_search_event(event, self.create_connection)
                for i in all_region_results:
                    make_region_obj = Region(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                    yield events.RegionSearchResultEvent(make_region_obj)
            yield engine_start_region_search_event(event, self.create_connection)
        elif isinstance(event, events.LoadRegionEvent):
            yield engine_region_loaded_event(event, self.create_connection)
        elif isinstance(event, events.SaveNewRegionEvent):
            yield engine_save_new_region_event(event, self.create_connection)
        elif isinstance(event, events.SaveRegionEvent):
            yield engine_save_edited_region(event, self.create_connection)
        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.
        #yield from ()

