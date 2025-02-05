import json
import uuid

import pytest
from requests_mock import Mocker as RequestsMocker
from uagents_core.config import DEFAULT_ALMANAC_API_PATH, AgentverseConfig
from uagents_core.crypto import Identity
from uagents_core.envelope import Envelope
import urllib.parse

from fetchai import communication


@pytest.fixture
def identity() -> Identity:
    return Identity.from_seed("TESTING", 1)


class TestSendMessageToAgent:
    def test_happy_path(self, identity: Identity):
        agent_name = "agent_one"
        agentverse_config = AgentverseConfig()
        almanac_api = urllib.parse.urljoin(
            agentverse_config.url, DEFAULT_ALMANAC_API_PATH
        )
        # the endpoint where the agent endpoint lookup request is expected to be sent
        expected_endpoint_lookup_url = f"{almanac_api}/agents/"
        # the endpoint url path where the agent message is expected to be sent
        expected_agent_url_path = "/v1/hosting/submit"
        # the endpoint url where the agent message is expected to be sent
        expected_agent_url = f"{agentverse_config.url}{expected_agent_url_path}"

        with RequestsMocker() as mock:
            # mock request sent from uagents_core.utils.communication.lookup_endpoint_for_agent method
            #   that resolves agent url
            mock.get(
                expected_endpoint_lookup_url,
                json={
                    "endpoints": [{"url": expected_agent_url, "weight": 1}],
                },
            )
            # mock request sent from uagents_core.utils.communication.send_message method
            #   that sends the message to the agent url
            mock.post(expected_agent_url)

            communication.send_message_to_agent(
                identity,
                agent_name,
                {},
            )

        assert mock.call_count == 2
        assert mock.last_request.scheme == agentverse_config.http_prefix
        assert mock.last_request.netloc == agentverse_config.base_url
        assert mock.last_request.port == 443
        assert mock.last_request.path == "/v1/hosting/submit"

        payload = Envelope.model_validate_json(mock.last_request.text)
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
    def envelope(self, identity: Identity, payload: dict) -> Envelope:
        session_id = uuid.uuid4()
        json_payload = json.dumps(payload)

        content = Envelope(
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
