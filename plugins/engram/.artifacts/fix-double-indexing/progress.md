# Fix Double Indexing - Progress

## Status
Phase: 1 - Discovery
Started: 2026-01-11
Last Updated: 2026-01-11

## Current State
- [x] Phase 1: Discovery
- [ ] Phase 2: Codebase Exploration
- [ ] Phase 3: Clarifying Questions
- [ ] Phase 4: Architecture Design
- [ ] Phase 5: Implementation
- [ ] Phase 6: Quality Review
- [ ] Phase 7: Manual Testing Verification
- [ ] Phase 8: Summary

## Problem Statement
Content is being indexed twice in engram:
1. **Live indexing** via `live_indexer.py` on Stop hook events
2. **Batch sync** via CLI `engram sync` or during `engram init`

This causes:
- Duplicate chunks in ChromaDB with different IDs
- Noisy search results (same content appears multiple times)
- Wasted storage and embedding compute

## Root Causes Identified
1. Live indexer and batch sync use different ID generation schemes
2. No deduplication check before indexing
3. Marker files track line numbers, not message UUIDs
4. ChromaDB upserts only help if IDs match exactly

## Session Log
### Session 1 - 2026-01-11
- Started feature development
- Deep exploration of engram codebase completed
- Identified double indexing as highest priority issue
- Root causes: Different ID generation, no dedup, marker files track lines not UUIDs
