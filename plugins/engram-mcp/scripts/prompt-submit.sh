#!/usr/bin/env bash
# Prompt submit - detect resume intent and inject context
# Uses uvx for portable execution (no pre-install required)
#
# For faster startup, users can install persistently:
#   uv tool install git+https://github.com/astrosteveo/engram

cat | uvx --from git+https://github.com/astrosteveo/engram engram-prompt-submit
