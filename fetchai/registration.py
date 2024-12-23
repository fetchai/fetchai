import hashlib
import json

import requests
from typing import Optional, Union, List, Dict, Literal
from pydantic import BaseModel, Field
import time

from fetchai.crypto import Identity
from fetchai.logger import logger


DEFAULT_AGENTVERSE_URL = "https://agentverse.ai"
DEFAULT_ALMANAC_API_URL = DEFAULT_AGENTVERSE_URL + "/v1/almanac"
DEFAULT_MAILBOX_API_URL = DEFAULT_AGENTVERSE_URL + "/v1/agents"
DEFAULT_CHALLENGE_URL = DEFAULT_AGENTVERSE_URL + "/v1/auth/challenge"


class AgentEndpoint(BaseModel):
    url: str
    weight: int


class VerifiableModel(BaseModel):
    agent_address: str
    signature: Optional[str] = None
    timestamp: Optional[int] = None

    def sign(self, identity: Identity):
        self.timestamp = int(time.time())
        digest = self._build_digest()
        self.signature = identity.sign_digest(digest)

    def verify(self) -> bool:
        return self.signature is not None and Identity.verify_digest(
            self.agent_address, self._build_digest(), self.signature
        )

    def _build_digest(self) -> bytes:
        sha256 = hashlib.sha256()
        sha256.update(
            json.dumps(
                self.model_dump(exclude={"signature"}),
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
        return sha256.digest()


AgentType = Literal["mailbox", "proxy", "custom"]


class AgentRegistrationAttestation(VerifiableModel):
    protocols: List[str]
    endpoints: List[AgentEndpoint]
    metadata: Optional[Dict[str, Union[str, Dict[str, str]]]] = None


class RegistrationRequest(BaseModel):
    address: str
    challenge: str
    challenge_response: str
    agent_type: AgentType
    endpoint: Optional[str] = None


class RegistrationResponse(BaseModel):
    success: bool


class ChallengeRequest(BaseModel):
    address: str


class ChallengeResponse(BaseModel):
    challenge: str


class AgentUpdates(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    readme: Optional[str] = Field(default=None, max_length=80000)
    avatar_url: Optional[str] = Field(default=None, max_length=4000)
    agent_type: Optional[AgentType] = "custom"


def register_with_agentverse(
    identity: Identity,
    url: str,
    agentverse_token: str,
    agent_title: str,
    readme: str,
    *,
    protocol_digest: str = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
    almanac_api: Optional[str] = None,
    agent_type: AgentType = "custom",
):
    """
    Register the agent with the Agentverse API.
    :param identity: The identity of the agent.
    :param url: The URL endpoint for the agent
    :param protocol_digest: The digest of the protocol that the agent supports
    :param agentverse_token: The token to use to authenticate with the Agentverse API
    :param agent_title: The title of the agent
    :param readme: The readme for the agent
    :param almanac_api: The URL of the Almanac API (if different from the default)
    :return:
    """
    almanac_api = almanac_api or DEFAULT_ALMANAC_API_URL

    agent_address = identity.address
    registration_metadata = {
        "almanac_endpoint": almanac_api,
        "agent_title": agent_title,
        "agent_address": agent_address,
        "agent_endpoint": url,
        "protocol_digest": protocol_digest,
    }
    logger.info(
        "Registering with Almanac API",
        extra=registration_metadata,
    )

    # create the attestation
    attestation = AgentRegistrationAttestation(
        agent_address=agent_address,
        protocols=[protocol_digest],
        endpoints=[
            AgentEndpoint(url=url, weight=1),
        ],
        metadata=None,
    )

    # sign the attestation
    attestation.sign(identity)

    # submit the attestation to the API
    r = requests.post(
        f"{almanac_api}/agents",
        headers={"content-type": "application/json"},
        data=attestation.model_dump_json(),
    )
    r.raise_for_status()
    logger.debug(
        "Agent attestation submitted",
        extra=registration_metadata,
    )

    # check to see if the agent exists
    r = requests.get(
        f"{DEFAULT_MAILBOX_API_URL}/{agent_address}",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {agentverse_token}",
        },
    )

    # if it doesn't then create it
    if r.status_code == 404:
        logger.debug(
            "Agent did not exist on agentverse; registering it",
            extra=registration_metadata,
        )

        challenge_request = ChallengeRequest(address=identity.address)
        logger.debug(
            "Requesting mailbox access challenge",
            extra=registration_metadata,
        )
        r = requests.post(
            DEFAULT_CHALLENGE_URL,
            data=challenge_request.model_dump_json(),
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {agentverse_token}",
            },
        )
        r.raise_for_status()
        challenge = ChallengeResponse.model_validate_json(r.text)
        registration_payload = RegistrationRequest(
            address=identity.address,
            challenge=challenge.challenge,
            challenge_response=identity.sign(challenge.challenge.encode()),
            endpoint=url,
            agent_type=agent_type,
        ).model_dump_json()
        r = requests.post(
            DEFAULT_MAILBOX_API_URL,
            headers={
                "content-type": "application/json",
                "authorization": f"Bearer {agentverse_token}",
            },
            data=registration_payload,
        )
        if r.status_code == 409:
            logger.info(
                "Agent already registered with Agentverse",
                extra=registration_metadata,
            )
        else:
            r.raise_for_status()
            registration_response = RegistrationResponse.model_validate_json(r.text)
            if registration_response.success:
                logger.info(
                    f"Successfully registered as {agent_type} agent in Agentverse",
                    extra=registration_metadata,
                )

    # update the readme and the title of the agent to make it easier to find
    logger.debug(
        "Registering agent title and readme with Agentverse",
        extra=registration_metadata,
    )
    update = AgentUpdates(name=agent_title, readme=readme)
    r = requests.put(
        f"{DEFAULT_MAILBOX_API_URL}/{agent_address}",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {agentverse_token}",
        },
        data=update.model_dump_json(),
    )
    r.raise_for_status()
    logger.info(
        "Completed registering agent with Agentverse",
        extra=registration_metadata,
    )
