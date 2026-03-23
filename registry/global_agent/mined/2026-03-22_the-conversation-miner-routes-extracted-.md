---
title: The Conversation Miner routes extracted 'Gold' items to specific destinations based on a channel-based routing table.
date: 2026-03-22
context_node: conversation_miner
---

The Conversation Miner implements a robust routing table that directs extracted 'Gold' items to specific destinations based on their `channel` flag. For example, `linkedin` items go to drafts, `colophon` items are appended, `internal` items are pushed to ChromaDB, and `law` items are stored as candidates.