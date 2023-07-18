import pytest
import responses

from ms_python_client.cern_ms_api_client import CERNMSApiClient
from ms_python_client.components.events.cern_events_component import (
    CERNEventsComponents,
    NotFoundError,
)
from ms_python_client.utils.event_generator import (
    EventParameters,
    PartialEventParameters,
)
from tests.ms_python_client.base_test_case import TEST_API_ENDPOINT, BaseTest, mock_msal


class TestEventsComponent(BaseTest):
    @mock_msal()
    def setUp(self) -> None:
        cern_ms_client = CERNMSApiClient(
            "account_id", "client_id", "client_secret", api_endpoint=TEST_API_ENDPOINT
        )
        self.events_component = CERNEventsComponents(cern_ms_client)
        return super().setUp()

    @responses.activate
    def test_list_events(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={"response": "ok"},
            status=200,
        )
        headers = {
            "test": "test",
        }
        events_list = self.events_component.list_events(
            "user_id", extra_headers=headers
        )
        assert events_list["response"] == "ok"
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_get_event_by_zoom_id_0(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={"@odata.count": 0},
            status=200,
        )
        with pytest.raises(NotFoundError):
            self.events_component.get_event_by_zoom_id("user_id", "zoom_id")

    @responses.activate
    def test_get_event_by_zoom_id_1(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={
                "@odata.count": 2,
                "value": [{"subject": "zoom_id_1"}, {"subject": "zoom_id_2"}],
            },
            status=200,
        )
        headers = {
            "test": "test",
        }
        result = self.events_component.get_event_by_zoom_id(
            "user_id", "zoom_id_1", headers
        )
        assert result["subject"] == "zoom_id_1"
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_create_event(self):
        responses.add(
            responses.POST,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={"response": "ok"},
            status=200,
        )
        event_parameters = EventParameters(
            zoom_url="https://zoom.us/j/1234567890",
            zoom_id="1234567890",
            subject="Test Event",
            start_time="2021-01-01T00:00:00",
            end_time="2021-01-01T01:00:00",
        )
        headers = {
            "test": "test",
        }
        event = self.events_component.create_event("user_id", event_parameters, headers)
        assert event["response"] == "ok"
        assert responses

    @responses.activate
    def test_update_event(self):
        responses.add(
            responses.PATCH,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events/event_id",
            json={"response": "ok"},
            status=200,
        )
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={
                "@odata.count": 1,
                "value": [{"id": "event_id", "subject": "Test Event"}],
            },
            status=200,
        )
        event_parameters = PartialEventParameters(
            zoom_url="https://zoom.us/j/1234567890",
            zoom_id="1234567890",
            subject="Test Event",
            start_time="2021-01-01T00:00:00",
            end_time="2021-01-01T01:00:00",
        )
        headers = {
            "test": "test",
        }
        event = self.events_component.update_event_by_zoom_id(
            "user_id", event_parameters, headers
        )
        assert event["response"] == "ok"
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_delete_event(self):
        responses.add(
            responses.DELETE,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events/event_id",
            status=204,
        )
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events",
            json={
                "@odata.count": 1,
                "value": [{"id": "event_id", "subject": "Test Event"}],
            },
            status=200,
        )
        headers = {
            "test": "test",
        }
        self.events_component.delete_event_by_zoom_id("user_id", "zoom_id", headers)
        assert responses.calls[0].request.headers["test"] == "test"

    @responses.activate
    def test_get_event_zoom_id(self):
        responses.add(
            responses.GET,
            f"{TEST_API_ENDPOINT}/users/user_id/calendar/events/event_id",
            json={
                "id": "event_id",
                "subject": "Test Event",
                "singleValueExtendedProperties": [
                    {
                        "id": "String {66f5a359-4659-4830-9070-00040ec6ac6e} Name ZoomId",
                        "value": "1234567890",
                    }
                ],
            },
            status=200,
        )
        headers = {
            "test": "test",
        }
        zoom_id = self.events_component.get_event_zoom_id(
            "user_id", "event_id", headers
        )
        assert zoom_id == "1234567890"
        assert responses.calls[0].request.headers["test"] == "test"
