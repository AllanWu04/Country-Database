from p2app import events
import sqlite3

def create_connection(event):
    """Create a connection with our database"""
    event_pth = event.path()
    connection = sqlite3.connect(event_pth)
    return connection

def engine_open_event(view_event):
    """This will take the view_event and open the file on the engine side."""
    event_pth = view_event.path()
    if event_pth.name.endswith(".db"):
        connect = create_connection(view_event)
        return events.DatabaseOpenedEvent(event_pth)
    else:
        return events.DatabaseOpenFailedEvent("Sorry, this file is invalid!")


