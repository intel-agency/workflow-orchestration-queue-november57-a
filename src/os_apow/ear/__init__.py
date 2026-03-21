"""The Ear module - Webhook receiver for GitHub events.

This module implements the webhook ingestion layer (The Ear) of the Four-Pillar Architecture.
It provides secure webhook endpoints with HMAC verification and event triage.
"""

from os_apow.ear.hmac import verify_github_signature
from os_apow.ear.routes import router as webhook_router

__all__ = ["verify_github_signature", "webhook_router"]
