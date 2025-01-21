import json
import uuid

import pytest
from requests_mock import Mocker as RequestsMocker

from fetchai import communication
from fetchai.crypto import Identity


@pytest.fixture
def identity() -> Identity:
    return Identity.from_seed("TESTING", 1)


def fake_agent_lookup_function(agent_address: str) -> str:
    """A fake agent look up function to use in test.

    Returns a predictable URL for testing against"""

    return f"http://localhost/fake_endpoint/{agent_address}"


class TestSendMessageToAgent:
    def test_happy_path(self, identity: Identity):
        agent_name = "agent_one"
        expected_url = "http://localhost/fake_endpoint/agent_one"

        with RequestsMocker() as mock:
            mock.post(expected_url)
            communication.send_message_to_agent(
                identity,
                agent_name,
                {},
                agent_lookup_function=fake_agent_lookup_function,
            )

            assert mock.called_once


class TestParseMessageFromAgent:
    @pytest.fixture
    def payload(self) -> dict:
        return {"hello": "there"}

    @pytest.fixture
    def envelope(self, identity: Identity, payload: dict) -> communication.Envelope:
        session_id = uuid.uuid4()
        json_payload = json.dumps(payload)

        content = communication.Envelope(
            version=1,
            sender=identity.address,
            target="agent_two",
            session=session_id,
            schema_digest="model:42",
            protocol_digest="protocol:42",
        )
        content.encode_payload(json_payload)
        content.sign(identity)

        return content

    def test_happy_path(self, envelope: communication.Envelope, payload: dict):
        agent_message = communication.parse_message_from_agent(
            envelope.model_dump_json()
        )

        assert (
            agent_message.sender
            == "agent1qv8qnqv4ddslkktlalqhv4zz7wsjnwslv0h33gpwh7fhw3txae2lg89awsp"
        )
        assert agent_message.target == "agent_two"
        assert agent_message.payload == payload
