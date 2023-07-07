import responses

from ms_python_client.components.events.events_component import EventsComponent
from ms_python_client.ms_api_client import MSApiClient
from ms_python_client.utils.event_generator import EventParameters
from tests.ms_python_client.base_test_case import TEST_API_ENDPOINT, BaseTest, mock_msal


class TestEventsComponent(BaseTest):
    @mock_msal()
    def setUp(self) -> None:
        ms_client = MSApiClient(
            "account_id", "client_id", "client_secret", api_endpoint=TEST_API_ENDPOINT
        )
        self.events_component = EventsComponent(ms_client)
        return super().setUp()

    @responses.activate
    def test_list_events(self):
        responses.add(
            responses.GET,
            "http://localhost/users/user_id/calendar/events",
            json={"response": "ok"},
            status=200,
        )
        events_list = self.events_component.list_events("user_id")
        assert events_list["response"] == "ok"

    @responses.activate
    def test_get_event(self):
        responses.add(
            responses.GET,
            "http://localhost/users/user_id/calendar/events/event_id",
            json={"response": "ok"},
            status=200,
        )
        event = self.events_component.get_event("user_id", "event_id")
        assert event["response"] == "ok"

    @responses.activate
    def test_create_event(self):
        responses.add(
            responses.POST,
            "http://localhost/users/user_id/calendar/events",
            json={"response": "ok"},
            status=200,
        )
        event_parameters = EventParameters(
            zoom_url="https://zoom.us/j/1234567890",
            indico_event_id="1234567890",
            subject="Test Event",
            start_time="2021-01-01T00:00:00",
            end_time="2021-01-01T01:00:00",
        )
        event = self.events_component.create_event("user_id", event_parameters)
        assert event["response"] == "ok"

    @responses.activate
    def test_update_event(self):
        responses.add(
            responses.PATCH,
            "http://localhost/users/user_id/calendar/events/event_id",
            json={"response": "ok"},
            status=200,
        )
        event_parameters = EventParameters(
            zoom_url="https://zoom.us/j/1234567890",
            indico_event_id="1234567890",
            subject="Test Event",
            start_time="2021-01-01T00:00:00",
            end_time="2021-01-01T01:00:00",
        )
        event = self.events_component.update_event(
            "user_id", "event_id", event_parameters
        )
        assert event["response"] == "ok"

    @responses.activate
    def test_delete_event(self):
        responses.add(
            responses.DELETE,
            "http://localhost/users/user_id/calendar/events/event_id",
            status=204,
        )
        self.events_component.delete_event("user_id", "event_id")
