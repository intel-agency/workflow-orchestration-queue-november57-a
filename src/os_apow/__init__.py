"""
OS-APOW - Autonomous AI Development Orchestrator.

This package implements a Four-Pillar Architecture for autonomous AI-driven development:
- The Ear (Notifier): FastAPI webhook receiver for GitHub events
- The State (Work Queue): Redis-backed state management
- The Brain (Sentinel): GitHub integration and orchestration logic
- The Hands (Worker): Execution layer via opencode CLI
"""

__version__ = "0.1.0"
__author__ = "Intel Agency"
