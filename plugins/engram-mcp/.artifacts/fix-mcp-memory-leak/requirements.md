# Fix MCP Server Memory Leak - Requirements

## Problem Statement

The `self.memories` dict in `EngramMCPServer` grows unbounded, accumulating `ProjectMemory` instances forever. Each instance holds a ChromaDB client with file handles and memory.

## Requirements

### R1: LRU Cache for ProjectMemory Instances
- **Decision:** Use LRU (Least Recently Used) eviction strategy
- **Max Size:** 5 projects
- **Behavior:** When cache is full, evict least recently used project before adding new one

### R2: Bounded Memory Usage
- **Goal:** Predictable memory footprint regardless of how many projects are accessed
- **Metric:** Maximum 5 ProjectMemory instances in memory at any time

## Non-Requirements (Out of Scope)
- TTL-based expiration (adds complexity)
- Configurable cache size (can add later if needed)
- Metrics/monitoring for cache hits/misses

## Success Criteria
1. `self.memories` dict never exceeds 5 entries
2. Most recently used projects remain cached
3. No change to MCP tool behavior (transparent to users)
4. No performance regression for typical usage patterns
