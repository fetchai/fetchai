import json
import uuid

import pytest
from requests_mock import Mocker as RequestsMocker

import fetchai.schema
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
        expected_url = fake_agent_lookup_function(agent_name)

        with RequestsMocker() as mock:
            mock.post(expected_url)
            communication.send_message_to_agent(
                identity,
                agent_name,
                {},
                agent_lookup_function=fake_agent_lookup_function,
            )

        assert mock.called_once
        assert mock.last_request.scheme == "http"
        assert mock.last_request.netloc == "localhost"
        assert mock.last_request.port == 80
        assert mock.last_request.path == f"/fake_endpoint/{agent_name}"

        payload = fetchai.schema.Envelope.model_validate_json(mock.last_request.text)
        assert (
            payload.protocol_digest
            == "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2"
        )
        assert (
            payload.sender
            == "agent1qv8qnqv4ddslkktlalqhv4zz7wsjnwslv0h33gpwh7fhw3txae2lg89awsp"
        )
        assert payload.target == "agent_one"
        assert payload.payload == "e30="


class TestParseMessageFromAgent:
    @pytest.fixture
    def payload(self) -> dict:
        return {"hello": "there"}

    @pytest.fixture
    def envelope(self, identity: Identity, payload: dict) -> fetchai.schema.Envelope:
        session_id = uuid.uuid4()
        json_payload = json.dumps(payload)

        content = fetchai.schema.Envelope(
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

    def test_happy_path(self, envelope: fetchai.schema.Envelope, payload: dict):
        agent_message = communication.parse_message_from_agent(
            envelope.model_dump_json()
        )

        assert (
            agent_message.sender
            == "agent1qv8qnqv4ddslkktlalqhv4zz7wsjnwslv0h33gpwh7fhw3txae2lg89awsp"
        )
        assert agent_message.target == "agent_two"
        assert agent_message.payload == payload


class TestParseMessageFromAgentDict:
    @pytest.fixture
    def payload(self) -> dict:
        return {
            "question": "Buy me a pair of shoes",
            "shoe_size": 12,
            "favorite_color": "black",
        }

    @pytest.fixture
    def content(self) -> dict:
        return {
            "version": 42,
            "sender": "agent1qtuj7h0tas4clwym5ckdrven78lz6afqwe7uyu3c5smw8sygnsvl6x6p52m",
            "target": "agent1qtuj7h0tas4clwym5ckdrven78lz6afqwe7uyu3c5smw8sygnsvl6x6p52m",
            "session": "7842f054-5c50-4344-98f4-dc55ef923bf8",
            "schema_digest": "model:708d789bb90924328daa69a47f7a8f3483980f16a1142c24b12972a2e4174bc6",
            "protocol_digest": "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
            "payload": "eyJxdWVzdGlvbiI6IkJ1eSBtZSBhIHBhaXIgb2Ygc2hvZXMiLCJzaG9lX3NpemUiOjEyLCJmYXZvcml0ZV9jb2xvciI6ImJsYWNrIn0=",
            "signature": "sig1jfjr6gfug8yfzwdwc4u5t2pz3zch0yx7xt68zfw4lsygg9nv3twzwsn9ala5e5wh4ywsf5d0lh6la2uz5rw3zkcevqcq7dcylp0syfgner05t",
        }

    def test_happy_path(self, content: dict, payload: dict):
        agent_message = communication.parse_message_from_agent_message_dict(content)

        assert agent_message.payload == payload
