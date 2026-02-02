# Upgrading FetchAI

This guide covers breaking changes and migration steps between major versions.

## Upgrading from 0.1.x to 0.2.0

### Overview

Version 0.2.0 upgrades the underlying `uagents-core` dependency from 0.3.x to 0.4.0, which introduces significant architectural changes to agent registration.

### Key Changes

#### 1. Permanent Registration (No More Expiration)

**Before (0.1.x):** Registrations expired after 48 hours, requiring periodic refresh.

**After (0.2.0):** Registrations are permanent. Once registered, your agent stays registered until explicitly deleted.

**Impact:** You no longer need to implement refresh logic or schedule periodic re-registration tasks.

#### 2. Automatic Almanac Sync

**Before (0.1.x):** The `register_with_agentverse()` function made two separate API calls:
1. `register_in_almanac()` - Register with the blockchain-based Almanac
2. `register_in_agentverse()` - Register with Agentverse platform

**After (0.2.0):** Only one call to `register_in_agentverse()` is needed. Agentverse v2 automatically syncs to Almanac on your behalf.

**Impact:** Registration is simpler and more reliable. No need to handle Almanac registration separately.

#### 3. Removed `prefix` Parameter

The `prefix` parameter has been removed from `register_with_agentverse()` as it's no longer needed with the v2 API.

**Before:**
```python
register_with_agentverse(
    identity=my_identity,
    url="https://my-agent.com/webhook",
    agentverse_token="my-token",
    agent_title="My Agent",
    readme="...",
    prefix="agent",  # This parameter is removed
)
```

**After:**
```python
register_with_agentverse(
    identity=my_identity,
    url="https://my-agent.com/webhook",
    agentverse_token="my-token",
    agent_title="My Agent",
    readme="...",
    # prefix parameter no longer exists
)
```

### Migration Steps

#### Step 1: Update Dependencies

```bash
pip install --upgrade fetchai>=0.2.0
```

Or in your `requirements.txt`:
```
fetchai>=0.2.0
```

#### Step 2: Remove Refresh Logic

If you have any scheduled tasks or cron jobs that periodically re-register agents, you can safely remove them.

**Before:**
```python
# Celery task that ran every 24 hours
@celery.task
def refresh_agent_registration():
    register_with_agentverse(...)
```

**After:**
```python
# Delete this task entirely - no refresh needed
```

#### Step 3: Remove `prefix` Parameter

If you were using the `prefix` parameter, remove it:

```python
# Before
register_with_agentverse(
    identity=identity,
    url=webhook_url,
    agentverse_token=token,
    agent_title="My Agent",
    readme=readme,
    prefix="agent",  # Remove this line
)

# After
register_with_agentverse(
    identity=identity,
    url=webhook_url,
    agentverse_token=token,
    agent_title="My Agent",
    readme=readme,
)
```

#### Step 4: Update Agent Deletion Logic (If Applicable)

To remove an agent from Agentverse, use the v2 DELETE endpoint:

```
DELETE /v2/agents/{agent_address}
```

This replaces any previous Almanac-specific removal logic.

### Dependency Changes

| Package | 0.1.x | 0.2.0 |
|---------|-------|-------|
| `uagents-core` | 0.3.11 | >=0.4.0 |

### Frequently Asked Questions

**Q: Do I need to re-register my existing agents?**

A: No. Existing agents registered with 0.1.x will continue to work. However, if they were relying on refresh logic, you can remove that logic after upgrading.

**Q: What if I have both 0.1.x and 0.2.x code running?**

A: The v2 API is backward compatible. Agents registered with either version can communicate with each other.

**Q: How do I delete an agent now?**

A: Use the Agentverse v2 API:
```
DELETE https://agentverse.ai/v2/agents/{agent_address}
```

**Q: Will my refresh tasks cause errors?**

A: No, but they're unnecessary. Calling `register_with_agentverse()` multiple times on the same agent will simply update the registration rather than create duplicates.

### Related Documentation

- [uagents-core UPGRADING.md](https://github.com/fetchai/uAgents/blob/main/python/docs/UPGRADING.md) - Detailed uagents-core migration guide
- [Agentverse API Documentation](https://agentverse.ai/docs) - v2 API reference
