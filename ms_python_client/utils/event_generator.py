import datetime
from typing import TypedDict


class BaseEventParameters(TypedDict):
    """Base parameters for creating an event

    Args:
        indico_event_id (str): The indico event id
    """

    indico_event_id: str


class OptionalTimezone(TypedDict, total=False):
    """Optional timezone parameter for creating an event

    Args:
        timezone (str): The timezone of the event
    """

    timezone: str


class EventParameters(BaseEventParameters, OptionalTimezone):
    """Parameters for creating an event

    Args:
        zoom_url (str): The Zoom URL for the event
        subject (str): The subject of the event
        start_time (str): The start time of the event in **ISO format**
        end_time (str): The end time of the event in **ISO format**
    """

    zoom_url: str
    subject: str
    start_time: str
    end_time: str


class PartialEventParameters(BaseEventParameters, OptionalTimezone, total=False):
    """Parameters for updating an event

    Args:
        zoom_url (str): The Zoom URL for the event
        subject (str): The subject of the event
        start_time (str): The start time of the event in **ISO format**
        end_time (str): The end time of the event in **ISO format**
    """

    zoom_url: str
    subject: str
    start_time: str
    end_time: str


def create_event_body(event_parameters: EventParameters) -> dict:
    """Creates an event from the given parameters

    Args:
        event_parameters (EventParameters): The parameters of the event

    Returns:
        Event: The event
    """

    timezone = event_parameters.get("timezone", "Europe/Zurich")

    return {
        "subject": f"[{event_parameters['indico_event_id']}] {event_parameters['subject']}",
        "body": {
            "contentType": "text",
            "content": f"Zoom URL: {event_parameters['zoom_url']}",
        },
        "start": {
            "dateTime": datetime.datetime.fromisoformat(
                event_parameters["start_time"]
            ).isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": datetime.datetime.fromisoformat(
                event_parameters["end_time"]
            ).isoformat(),
            "timeZone": timezone,
        },
        "location": {
            "displayName": event_parameters["zoom_url"],
            "locationType": "default",
            "uniqueIdType": "private",
            "uniqueId": event_parameters["zoom_url"],
        },
        "attendees": [],
        "allowNewTimeProposals": False,
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "unknown",
        "onlineMeetingUrl": event_parameters["zoom_url"],
    }


def create_partial_event_body(event_parameters: PartialEventParameters) -> dict:
    """Updates an event from the given parameters

    Args:
        event_parameters (PartialEventParameters): The parameters of the event

    Returns:
        Event: The event
    """
    event = {}

    timezone = event_parameters.get("timezone", "Europe/Zurich")

    if "zoom_url" in event_parameters:
        event.update(
            {
                "body": {
                    "contentType": "text",
                    "content": f"Zoom URL: {event_parameters['zoom_url']}",
                },
                "location": {
                    "displayName": event_parameters["zoom_url"],
                    "locationType": "default",
                    "uniqueIdType": "private",
                    "uniqueId": event_parameters["zoom_url"],
                },
                "onlineMeetingUrl": event_parameters["zoom_url"],
            }
        )

    if "subject" in event_parameters:
        event.update(
            {
                "subject": f"[{event_parameters['indico_event_id']}] {event_parameters['subject']}"
            }
        )

    if "start_time" in event_parameters:
        event.update(
            {
                "start": {
                    "dateTime": datetime.datetime.fromisoformat(
                        event_parameters["start_time"]
                    ).isoformat(),
                    "timeZone": timezone,
                }
            }
        )

    if "end_time" in event_parameters:
        event.update(
            {
                "end": {
                    "dateTime": datetime.datetime.fromisoformat(
                        event_parameters["end_time"]
                    ).isoformat(),
                    "timeZone": timezone,
                }
            }
        )

    return event