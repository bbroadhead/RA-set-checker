# NeoStation export contract (v1)

Export a complete library snapshot as UTF-8 JSON:
```json
{"format":"neostation-ra-library","version":1,"entries":[{"consoleId":1,"hash":"8bd4a97783cda077c342173df0a9b51e"}]}
```
The sample hash is illustrative. Each entry represents an actual locally available game file and a computed RetroAchievements-compatible hash. Console IDs are official RA numeric system IDs, not local platform IDs. Hashes are 32 hexadecimal characters, normalized to lowercase. Do not substitute whole-file MD5 for platform-specific RA hashing, or copy an approved hash from a manually mapped game. Include valid computed hashes even if unmatched or unsupported by the current catalog. Deduplicate by consoleId and hash. Omit failed/unavailable files and report them separately. Never include API credentials or absolute local paths. Optional metadata is ignored by the importer.

Import replaces the previous imported snapshot, with confirmation, while preserving manual title and hash ownership. Imports are matched against the pair (consoleId, hash), not game names. Unmatched hashes remain stored and can match later catalog updates. Export a full library rather than a filtered subset to avoid unintentionally removing imported ownership. Browser storage is local; use the separate backup feature to transfer progress.
