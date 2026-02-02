from unittest import mock

import pytest
from uagents_core.config import AgentverseConfig
from uagents_core.identity import Identity

from fetchai.registration import register_with_agentverse
from fetchai.schema import AgentGeoLocation


class TestRegisterWithAgentverse:
    @pytest.fixture
    def identity(self) -> Identity:
        return Identity.from_seed("TESTING", 1)

    @pytest.fixture
    def registration_params(self, identity: Identity) -> dict:
        return {
            "identity": identity,
            "url": "https://api.sampleurl.com/webhook",
            "agentverse_token": "test_token",
            "agent_title": "Test Agent",
            "readme": "README content",
        }

    @pytest.fixture
    def mock_agentverse_config(self) -> mock.Mock:
        return mock.create_autospec(AgentverseConfig, instance=True)

    def test_returns_true_when_registration_succeeds(self, registration_params: dict):
        """Test successful registration with v2 API."""
        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=True
        ) as mock_agentverse:
            result = register_with_agentverse(**registration_params)

            assert result is True
            assert mock_agentverse.call_count == 1

    def test_returns_false_when_registration_fails(self, registration_params: dict):
        """Test failed registration returns False."""
        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=False
        ) as mock_agentverse:
            result = register_with_agentverse(**registration_params)

            assert result is False
            assert mock_agentverse.call_count == 1

    def test_calls_register_in_agentverse_with_correct_parameters(
        self, registration_params: dict
    ):
        """Test that register_in_agentverse is called with correct parameters."""
        geo_location = AgentGeoLocation(latitude=51.5074, longitude=-0.1278, radius=1.0)
        metadata = {"test_key": "test_value"}

        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=True
        ) as mock_agentverse:
            register_with_agentverse(
                geo_location=geo_location,
                metadata=metadata,
                agent_type="custom",
                **registration_params,
            )

            mock_agentverse.assert_called_once()
            call_args = mock_agentverse.call_args

            # Verify connect request
            assert (
                call_args.kwargs["request"].user_token
                == registration_params["agentverse_token"]
            )
            assert call_args.kwargs["request"].agent_type == "custom"
            assert call_args.kwargs["request"].endpoint == registration_params["url"]

            # Verify identity
            assert call_args.kwargs["identity"] == registration_params["identity"]

            # Verify agent details (AgentverseRegistrationRequest)
            agent_details = call_args.kwargs["agent_details"]
            assert agent_details.name == registration_params["agent_title"]
            assert agent_details.readme == registration_params["readme"]
            assert agent_details.endpoint == registration_params["url"]

    def test_handles_proxy_agent_type_correctly(
        self, registration_params: dict, mock_agentverse_config: mock.Mock
    ):
        """Test that proxy agent type uses the proxy endpoint for both requests."""
        with (
            mock.patch(
                "fetchai.registration.register_in_agentverse", return_value=True
            ) as mock_agentverse,
            mock.patch(
                "fetchai.registration.AgentverseConfig",
                return_value=mock_agentverse_config,
            ),
        ):
            register_with_agentverse(agent_type="proxy", **registration_params)

            call_args = mock_agentverse.call_args

            # For proxy type, both requests should use the proxy endpoint
            agent_details = call_args.kwargs["agent_details"]
            connect_request = call_args.kwargs["request"]

            assert agent_details.endpoint == mock_agentverse_config.proxy_endpoint
            assert connect_request.endpoint == mock_agentverse_config.proxy_endpoint

    def test_metadata_is_public_overridden_by_function_parameter(
        self, registration_params: dict
    ):
        """Test that is_public in metadata is overridden by function parameter."""
        metadata_with_conflicts = {
            "is_public": "False",
            "other_key": "other_value",
        }

        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=True
        ) as mock_agentverse:
            register_with_agentverse(
                metadata=metadata_with_conflicts,
                is_public=True,
                **registration_params,
            )

            call_args = mock_agentverse.call_args
            agent_details = call_args.kwargs["agent_details"]
            final_metadata = agent_details.metadata

            assert final_metadata["is_public"] == "True"
            assert final_metadata["other_key"] == "other_value"

    def test_geolocation_added_to_metadata(self, registration_params: dict):
        """Test that geolocation is properly added to metadata."""
        geo_location = AgentGeoLocation(latitude=51.5074, longitude=-0.1278)

        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=True
        ) as mock_agentverse:
            register_with_agentverse(
                geo_location=geo_location,
                **registration_params,
            )

            call_args = mock_agentverse.call_args
            agent_details = call_args.kwargs["agent_details"]
            final_metadata = agent_details.metadata

            assert "geolocation" in final_metadata
            assert final_metadata["geolocation"] == geo_location.as_str_dict()

    def test_geolocation_overrides_metadata_geolocation(
        self, registration_params: dict
    ):
        """Test that geo_location parameter overrides geolocation in metadata."""
        metadata_with_geo = {
            "geolocation": {"lat": "0", "lng": "0"},
        }
        geo_location = AgentGeoLocation(latitude=51.5074, longitude=-0.1278)

        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=True
        ) as mock_agentverse:
            register_with_agentverse(
                geo_location=geo_location,
                metadata=metadata_with_geo,
                **registration_params,
            )

            call_args = mock_agentverse.call_args
            agent_details = call_args.kwargs["agent_details"]
            final_metadata = agent_details.metadata

            # geo_location parameter should override metadata
            assert final_metadata["geolocation"] == geo_location.as_str_dict()

    def test_default_protocol_digest_is_chat_protocol(self, registration_params: dict):
        """Test that the default protocol digest is the chat protocol."""
        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=True
        ) as mock_agentverse:
            register_with_agentverse(**registration_params)

            call_args = mock_agentverse.call_args
            agent_details = call_args.kwargs["agent_details"]

            # Should contain the chat protocol digest
            expected_digest = (
                "proto:30a801ed3a83f9a0ff0a9f1e6fe958cb91da1fc2218b153df7b6cbf87bd33d62"
            )
            assert expected_digest in agent_details.protocols

    def test_custom_protocol_digest(self, registration_params: dict):
        """Test that a custom protocol digest can be specified."""
        custom_protocol = "proto:custom123"

        with mock.patch(
            "fetchai.registration.register_in_agentverse", return_value=True
        ) as mock_agentverse:
            register_with_agentverse(
                protocol_digest=custom_protocol,
                **registration_params,
            )

            call_args = mock_agentverse.call_args
            agent_details = call_args.kwargs["agent_details"]

            assert custom_protocol in agent_details.protocols
