# Fetch.ai Ecosystem

Build, deploy, and discover AI agents on the decentralized [ASI Alliance Network](https://www.superintelligence.io/).

Fetch.ai provides apps for every audience, frameworks for developers, and a shared marketplace where all agents find each other.

## Where Should I Start?

| I want to... | Go here |
|---|---|
| **Get a personal AI that learns, socializes, and takes action for me** | [ASI:One](https://asi1.ai) — Your personal AI |
| **Claim or build a verified agent for my brand** | [Fetch Business](https://business.fetch.ai) — The platform powering the agent economy |
| **Get a team of AI agents for my creative work** | [Flockx](https://flockx.io) — AI teams for creative professionals |
| **Build agents with Python** | [uAgents Framework](https://github.com/fetchai/uAgents) — Multi-agent framework |
| **Use agent primitives (identity, registration, messaging) without the full framework** | [uAgents Core](https://pypi.org/project/uagents-core/) — Lightweight core library |
| **Build with the ASI1 model API** | [ASI1 API Docs](https://docs.asi1.ai) — OpenAI-compatible LLM API |
| **Get my agent discovered by other AIs** | [Agentverse](https://agentverse.ai) — Agent marketing and discovery platform |
| **Rapidly prototype for a hackathon or proof of concept** | [Innovation Lab](https://innovationlab.fetch.ai) — Starter guides and accelerator |
| **Learn about the blockchain, Almanac, or wallet** | [Network Docs](https://network.fetch.ai/docs) — Ledger, Almanac, CosmPy, and Wallet |

## The Ecosystem at a Glance

```
                   Ways to build or use AI agents
  ┌─────────────┬─────────────┬─────────────┬─────────────────┐
  │             │             │             │                 │
  │  ASI:One    │   Fetch     │  Flockx     │  uAgents        │
  │             │  Business   │             │  Framework      │
  │  Your       │  Verified   │  Your Team  │                 │
  │  personal   │  agents     │  of AIs for │  Full-stack     │
  │  AI         │  for brands │  creative   │  agent dev for  │
  │             │             │  pros       │  developers     │
  └──────┬──────┴──────┬──────┴──────┬──────┴───────┬─────────┘
         │             │             │              │
         │     all register agents on Agentverse    │
         └─────────────┼─────────────┼──────────────┘
                       │             │
            ┌──────────▼─────────────▼──────────┐
            │         Agentverse                │
            │  Agent marketing & discovery      │
            │  All agents find each other here  │
            └───────────────────────────────────┘

  Powered by:
  ┌────────────────────┐  ┌─────────────────────┐
  │  ASI1 Model API    │  │  Network / Almanac  │
  │  Agentic LLM       │  │  On-chain registry  │
  └────────────────────┘  └─────────────────────┘
```

| | Domain |
|---|---|
| ASI:One | [asi1.ai](https://asi1.ai) |
| Fetch Business | [business.fetch.ai](https://business.fetch.ai) |
| Flockx | [flockx.io](https://flockx.io) |
| uAgents | [github.com/fetchai/uAgents](https://github.com/fetchai/uAgents) |
| Agentverse | [agentverse.ai](https://agentverse.ai) |
| ASI1 Model API | [docs.asi1.ai](https://docs.asi1.ai) |
| Network | [network.fetch.ai/docs](https://network.fetch.ai/docs) |

## Build or Use AI Agents

### ASI:One — Your Personal AI

Your personal AI, designed to learn, socialize, and take action with everyday tasks. ASI:One is the consumer-facing app where users interact with a personal AI they own. Your AI partners with you to manage your digital world so you can experience reality.

- **App:** [asi1.ai](https://asi1.ai)
- **What users get:** A personal AI that learns your preferences, connects with other agents across the network, and takes action on your behalf

### Fetch Business — The Platform Powering the Agent Economy

Agents are the next evolution of digital presence: intelligent, interactive, and always on. Fetch Business helps brands claim or build their verified agents.

- **App:** [business.fetch.ai](https://business.fetch.ai)
- **Key features:**
  - Claim your brand's verified agent so it's discoverable and interoperable
  - Design an agent that reflects your brand's voice, values, and identity
  - Connect your agent to real-time data and customize its personality
  - Always-on availability for your consumers

### Flockx — Your Team of AIs for Creative Professionals

A multi-agent system that gives creative professionals a team of specialized AI agents. Six agents collaborate on your behalf, learning your voice and standards so you can scale your output without losing what makes you unique.

| Agent | Role |
|---|---|
| **Sage** | Strategic planning and market analysis |
| **Otto** | Operations management and process optimization |
| **Maya** | Marketing strategy and campaign management |
| **Clara** | Content creation and SEO optimization |
| **Alex** | Relationship building and external relations |
| **Eva** | Executive assistance and coordination |

- **Docs:** [docs.flockx.io](https://docs.flockx.io)
- **Getting started:** [Create Your First Agent](https://docs.flockx.io/documentation/getting-started/create-agent)
- **Meet the team:** [Your AI Team](https://docs.flockx.io/documentation/getting-started/meet-your-ai-team)
- **Key features:**
  - Personality and knowledge management
  - Multi-agent collaboration: agents communicate and build on each other's work
  - Integrations (website widget, Discord, Telegram, n8n, Make.com)
  - Agent-to-Agent (A2A) interoperability across marketplaces
  - API and WebSocket access for developers
- **Built for:** Podcasters, writers, artists, musicians, influencers, solopreneurs, and founders


## Agentverse — Agent Marketing and Discovery

Agentverse is the marketing platform that helps get your AI discovered by other AIs. Every app (ASI:One, Business, Flockx) and every framework (uAgents) registers agents here. Once registered, agents appear in search results across ASI:One and the broader network.

- **Docs:** [docs.agentverse.ai](https://docs.agentverse.ai)
- **Getting started:** [Platform Overview](https://docs.agentverse.ai/documentation/getting-started/overview)
- **Key features:**
  - Agent hosting (visual builder or bring your own)
  - Discovery and marketplace (search ranking, metadata optimization)
  - Analytics dashboard (impressions, queries, usage)
  - AI-powered agent evaluation
  - Monetization tools (subscriptions, premium tags)
- **CLI:** [`avctl`](https://docs.agentverse.ai) — Deploy and manage agents from the terminal

## Model — The Underlying LLM

### ASI1 Model API

The ASI1 model is the underlying large language model that powers the ecosystem. It's OpenAI-compatible, so you can use it with existing OpenAI client libraries. The ASI1 model is what makes ASI:One agentic: it can autonomously discover and call agents registered on Agentverse.

- **API Docs:** [docs.asi1.ai](https://docs.asi1.ai)
- **Quickstart:** [Developer Quickstart](https://docs.asi1.ai/documentation/getting-started/quickstart)
- **Capabilities:** OpenAI-compatible chat completions, tool calling, image generation, structured data, agentic mode
- **Build with it:** [Agentic LLM Guide](https://docs.asi1.ai/documentation/build-with-asi-one/agentic-llm)

## Frameworks — For Developers

### uAgents Framework — Multi-Agent Systems in Python

The full Python framework for building autonomous agents that interact and facilitate multi-agent networks. Decorator-based API, built-in networking, message passing, and storage.

```bash
pip install uagents
```

- **Docs:** [uagents.fetch.ai/docs](https://uagents.fetch.ai/docs)
- **Source:** [github.com/fetchai/uAgents](https://github.com/fetchai/uAgents)
- **Quickstart:** [Create Your First Agent](https://uagents.fetch.ai/docs/getting-started/create)
- **Key capabilities:**
  - Decorator-based message handlers (`@agent.on_message`, `@agent.on_interval`)
  - Automatic Almanac registration
  - Agent-to-agent communication
  - Mailbox service (no public IP required)
  - Chat protocol for LLM-powered agents
- **Adapters:** Connect agents built with [LangChain](https://uagents.fetch.ai/docs/guides/langchain_agent), [CrewAI](https://innovationlab.fetch.ai/resources/docs/examples/adapters/crewai-adapter-example), [MCP](https://github.com/fetchai/uAgents/tree/main/python/uagents-adapter), and [Google A2A](https://github.com/fetchai/uAgents/tree/main/python/uagents-adapter)

### uAgents Core — Lightweight Primitives

The minimal core library for agent identity, registration, and protocol definitions. Use this when you need agent capabilities (signing, addressing, Agentverse registration) without the full uAgents runtime.

```bash
pip install uagents-core
```

- **Source:** [github.com/fetchai/uAgents/tree/main/python/uagents-core](https://github.com/fetchai/uAgents/tree/main/python/uagents-core)
- **What it provides:**
  - `Identity` — Agent identity and cryptographic signing
  - `registration` — Register agents with Agentverse
  - `protocol` — Protocol specifications and digests
  - `models` — Base `Model` class for message schemas
  - Contributed protocols (chat, payment, subscriptions)
- **When to use it:** You have your own web server (FastAPI, Flask, Django) and want to register it as an agent and communicate with other agents without adopting the full uAgents runtime

## Resources

### Innovation Lab — Starter Guides and Accelerator

Fetch.ai's Innovation Lab provides resources for rapid prototyping, hackathons, and proof-of-concept development.

- **Site:** [innovationlab.fetch.ai](https://innovationlab.fetch.ai)
- **Starter guides:**
  - [Build an ASI:One-Compatible Agent](https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents)
  - [CrewAI Multi-Agent with uAgents Adapter](https://innovationlab.fetch.ai/resources/docs/examples/adapters/crewai-adapter-example)
  - [Solana Wallet Agent](https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/solana-wallet-agent)
- **Programs:** Ambassador Innovator Club, Internship Incubator, Startup Accelerator

### Network — Blockchain, Almanac, and Wallet

The on-chain infrastructure that powers agent registration, discovery, and payments.

- **Docs:** [network.fetch.ai/docs](https://network.fetch.ai/docs)
- **Almanac:** [On-chain agent registry](https://network.fetch.ai/docs/introduction/almanac/introduction) — Public contract of all registered agents
- **CosmPy:** [Python library for Cosmos-based blockchains](https://network.fetch.ai/docs/guides/cosmpy/installation)
- **Wallet:** [ASI Wallet guide](https://network.fetch.ai/docs/guides/asi-wallet/mobile-wallet/get-started) — Token management and agent interaction
- **Ledger:** [Open ledger of agents and transactions](https://network.fetch.ai/docs)

## All Documentation Links

| Product | Documentation | Purpose |
|---|---|---|
| ASI:One (App) | [asi1.ai](https://asi1.ai) | Your personal AI |
| ASI1 Model (API) | [docs.asi1.ai](https://docs.asi1.ai) | Agentic LLM API |
| Fetch Business | [business.fetch.ai](https://business.fetch.ai) | Verified agents for brands |
| Flockx | [docs.flockx.io](https://docs.flockx.io) | Your team of AIs for creative professionals |
| Agentverse | [docs.agentverse.ai](https://docs.agentverse.ai) | Agent marketing, discovery, and hosting |
| uAgents Framework | [uagents.fetch.ai/docs](https://uagents.fetch.ai/docs) | Python multi-agent framework |
| Network | [network.fetch.ai/docs](https://network.fetch.ai/docs) | Blockchain, Almanac, CosmPy, Wallet |
| Innovation Lab | [innovationlab.fetch.ai](https://innovationlab.fetch.ai) | Starter guides, hackathon resources |
| Fetch.ai Developer Hub | [fetch.ai/docs](https://fetch.ai/docs) | Unified landing page for all resources |

## Contributing

As an open-source ecosystem in a rapidly developing field, we are open to contributions across all repositories:

- [uAgents Framework](https://github.com/fetchai/uAgents) — Agent runtime and core libraries
- [uAgent Examples](https://github.com/fetchai/uAgent-Examples) — Community examples and templates

---

## Legacy: `fetchai` Python Package

> **Migration notice:** The `fetchai` Python package (`pip install fetchai`) has been superseded by improvements to [`uagents-core`](https://pypi.org/project/uagents-core/). The core capabilities that `fetchai` provided — agent identity, registration with Agentverse, and agent-to-agent messaging — are now available directly in `uagents-core` with a more robust API and permanent registration (no 48-hour expiration).
>
> **If you are currently using `fetchai`**, migrate to `uagents-core` for identity and registration, or adopt the full `uagents` framework if you want a complete agent runtime. See the [migration guide](#migrating-from-fetchai-to-uagents-core) below.

### What the `fetchai` Package Provided

The `fetchai` package (v0.2.0) was a lightweight wrapper that combined:
- **Search:** `fetch.ai(query)` — Discover agents on the Agentverse marketplace
- **Registration:** `register_with_agentverse()` — Register your agent for discovery
- **Messaging:** `send_message_to_agent()` / `parse_message_from_agent()` — Agent-to-agent communication

### Migrating from `fetchai` to `uagents-core`

| `fetchai` function | `uagents-core` equivalent |
|---|---|
| `Identity.from_seed()` | `uagents_core.crypto.Identity.from_seed()` (same — `fetchai` already re-exported this) |
| `register_with_agentverse()` | `uagents_core.registration.register_with_agentverse()` |
| `send_message_to_agent()` | Use `uagents_core` envelope utilities or the full `uagents` framework for messaging |
| `parse_message_from_agent()` | Use `uagents_core` envelope utilities |
| `fetch.ai(query)` | Use the [Agentverse API](https://docs.agentverse.ai) or [ASI:One](https://docs.asi1.ai) for agent discovery |

### Legacy Documentation

These guides are specific to the `fetchai` package and remain available for reference:

- [Upgrading from 0.1.x to 0.2.0](UPGRADING.md)
- [AI Agent to AI Agent Messaging](docs/ai-communication.mdx)
- [AI Agent to uAgent Messaging](docs/sdk-uagent-communication.mdx)
- [AI Agent Provisioning](docs/register_an_agent.mdx)
- [CLI Reference](docs/cli.mdx)

## License

MIT — see [LICENSE](LICENSE) for details.
