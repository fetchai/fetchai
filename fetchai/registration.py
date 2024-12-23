import hashlib
import json

import requests
from typing import Optional, Union, List, Dict
from pydantic import BaseModel
import time

from fetchai.crypto import Identity
from fetchai.logging import logger


DEFAULT_AGENTVERSE_URL = "https://agentverse.ai"
DEFAULT_ALMANAC_API_URL = DEFAULT_AGENTVERSE_URL + "/v1/almanac"
DEFAULT_MAILBOX_API_URL = DEFAULT_AGENTVERSE_URL + "/v1/agents"


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


class AgentRegistrationAttestation(VerifiableModel):
    protocols: List[str]
    endpoints: List[AgentEndpoint]
    metadata: Optional[Dict[str, Union[str, Dict[str, str]]]] = None


def register_with_agentverse(
    identity: Identity,
    url: str,
    agentverse_token: str,
    agent_title: str,
    readme: str,
    *,
    protocol_digest: str = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
    almanac_api: Optional[str] = None,
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
        r = requests.post(
            f"{DEFAULT_MAILBOX_API_URL}/",
            headers={
                "content-type": "application/json",
                "authorization": f"Bearer {agentverse_token}",
            },
            json={
                "address": agent_address,
                "name": agent_title,
            },
        )
        r.raise_for_status()

    # update the readme and the title of the agent to make it easier to find
    logger.debug(
        "Registering agent title and readme with Agentverse",
        extra=registration_metadata,
    )
    r = requests.put(
        f"{DEFAULT_MAILBOX_API_URL}/{agent_address}",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {agentverse_token}",
        },
        json={
            "name": agent_title,
            "readme": readme,
        },
    )
    r.raise_for_status()
    logger.info(
        "Completed registering agent with Agentverse",
        extra=registration_metadata,
    )
