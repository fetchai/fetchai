# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-29

### Breaking Changes

- **Upgraded `uagents-core` from 0.3.11 to 0.4.0** - This is the primary driver for this major version bump
- **Removed `prefix` parameter** from `register_with_agentverse()` - No longer needed with v2 API
- **Removed `register_in_almanac()` call** - Agentverse v2 handles Almanac sync automatically

### Changed

- `register_with_agentverse()` now uses Agentverse v2 API exclusively
- Registration is now permanent (no 48-hour expiration)
- Simplified registration flow - single API call instead of two

### Removed

- Almanac-specific registration logic (handled automatically by Agentverse)
- `prefix` parameter from registration function

### Documentation

- Added `UPGRADING.md` with migration guide from 0.1.x to 0.2.0
- Added `CHANGELOG.md` for version history tracking

## [0.1.45] - Previous Release

### Notes

- Last version compatible with `uagents-core==0.3.11`
- Required periodic registration refresh (48-hour expiration)
- Required separate Almanac and Agentverse registration calls

---

For upgrade instructions, see [UPGRADING.md](UPGRADING.md).
