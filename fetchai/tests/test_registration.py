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

    def test_returns_true_when_both_registrations_succeed(
        self, registration_params: dict
    ):
        with (
            mock.patch(
                "fetchai.registration.register_in_almanac", return_value=True
            ) as mock_almanac,
            mock.patch(
                "fetchai.registration.register_in_agentverse", return_value=True
            ) as mock_agentverse,
        ):
            result = register_with_agentverse(**registration_params)

            assert result is True
            assert mock_almanac.call_count == 1
            assert mock_agentverse.call_count == 1

    def test_agentverse_not_called_if_almanac_fails(self, registration_params: dict):
        with (
            mock.patch(
                "fetchai.registration.register_in_almanac", return_value=False
            ) as mock_almanac,
            mock.patch(
                "fetchai.registration.register_in_agentverse"
            ) as mock_agentverse,
        ):
            result = register_with_agentverse(**registration_params)

            assert result is False
            assert mock_almanac.call_count == 1
            mock_agentverse.assert_not_called()

    def test_returns_false_when_agentverse_registration_fails(
        self, registration_params: dict
    ):
        with (
            mock.patch(
                "fetchai.registration.register_in_almanac", return_value=True
            ) as mock_almanac,
            mock.patch(
                "fetchai.registration.register_in_agentverse", return_value=False
            ) as mock_agentverse,
        ):
            result = register_with_agentverse(**registration_params)

            assert result is False
            assert mock_almanac.call_count == 1
            assert mock_agentverse.call_count == 1

    def test_calls_functions_with_correct_parameters(self, registration_params: dict):
        geo_location = AgentGeoLocation(latitude=51.5074, longitude=-0.1278, radius=1.0)
        metadata = {"test_key": "test_value"}

        with (
            mock.patch(
                "fetchai.registration.register_in_almanac", return_value=True
            ) as mock_almanac,
            mock.patch(
                "fetchai.registration.register_in_agentverse", return_value=True
            ) as mock_agentverse,
        ):
            register_with_agentverse(
                geo_location=geo_location,
                metadata=metadata,
                agent_type="proxy",
                **registration_params,
            )

            mock_almanac.assert_called_once()
            almanac_call_args = mock_almanac.call_args
            assert (
                almanac_call_args.kwargs["identity"] == registration_params["identity"]
            )
            assert almanac_call_args.kwargs["protocol_digests"] == [
                "proto:30a801ed3a83f9a0ff0a9f1e6fe958cb91da1fc2218b153df7b6cbf87bd33d62"
            ]
            expected_metadata = {
                "test_key": "test_value",
                "is_public": "True",
                "geolocation": geo_location.as_str_dict(),
            }
            assert almanac_call_args.kwargs["metadata"] == expected_metadata

            mock_agentverse.assert_called_once()
            agentverse_call_args = mock_agentverse.call_args
            assert (
                agentverse_call_args.kwargs["identity"]
                == registration_params["identity"]
            )
            assert (
                agentverse_call_args.kwargs["request"].user_token
                == registration_params["agentverse_token"]
            )
            assert agentverse_call_args.kwargs["request"].agent_type == "proxy"
            assert (
                agentverse_call_args.kwargs["request"].endpoint
                == registration_params["url"]
            )
            assert (
                agentverse_call_args.kwargs["agent_details"].name
                == registration_params["agent_title"]
            )
            assert (
                agentverse_call_args.kwargs["agent_details"].readme
                == registration_params["readme"]
            )

    def test_handles_proxy_agent_type_correctly(
        self, registration_params: dict, mock_agentverse_config: mock.Mock
    ):
        with (
            mock.patch(
                "fetchai.registration.register_in_almanac", return_value=True
            ) as mock_almanac,
            mock.patch(
                "fetchai.registration.register_in_agentverse", return_value=True
            ),
            mock.patch(
                "fetchai.registration.AgentverseConfig",
                return_value=mock_agentverse_config,
            ),
        ):
            register_with_agentverse(agent_type="proxy", **registration_params)

            almanac_call_args = mock_almanac.call_args
            assert almanac_call_args.kwargs["endpoints"] == [
                mock_agentverse_config.proxy_endpoint
            ]

    def test_metadata_is_public_and_geolocation_are_overridden_by_function_parameters(
        self, registration_params: dict
    ):
        metadata_with_conflicts = {
            "is_public": "False",
            "geolocation": {"lat": "0", "lng": "0"},
            "other_key": "other_value",
        }
        geo_location = AgentGeoLocation(latitude=51.5074, longitude=-0.1278)

        with (
            mock.patch(
                "fetchai.registration.register_in_almanac", return_value=True
            ) as mock_almanac,
            mock.patch(
                "fetchai.registration.register_in_agentverse", return_value=True
            ),
        ):
            register_with_agentverse(
                geo_location=geo_location,
                metadata=metadata_with_conflicts,
                is_public=True,
                **registration_params,
            )

            almanac_call_args = mock_almanac.call_args
            final_metadata = almanac_call_args.kwargs["metadata"]

            assert final_metadata["is_public"] == "True"
            assert final_metadata["geolocation"] == geo_location.as_str_dict()
            assert final_metadata["other_key"] == "other_value"
