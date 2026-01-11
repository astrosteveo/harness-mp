#!/usr/bin/env bash
# Live indexer wrapper - runs without requiring pip install
# Uses uvx to run the engram package directly

uvx --from "git+https://github.com/astrosteveo/engram" engram-live-index
