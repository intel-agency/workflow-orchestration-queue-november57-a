"""FastAPI routes for GitHub webhook handling.

This module defines the webhook endpoints for receiving GitHub events.
"""

import logging
from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, Request, status

from os_apow.config import Settings, get_settings
from os_apow.ear.hmac import verify_github_signature

logger = logging.getLogger(__name__)

router = APIRouter()


def verify_webhook_signature(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> bytes:
    """Verify the GitHub webhook signature.

    Args:
        request: The FastAPI request object.
        settings: Application settings.

    Returns:
        The raw request body bytes.

    Raises:
        HTTPException: If signature verification fails.
    """
    # Get the signature from headers
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Hub-Signature-256 header",
        )

    # Get the raw body
    body = cast("bytes", request.state.raw_body)

    # Verify signature if webhook secret is configured
    if settings.webhook_secret and not verify_github_signature(
        body=body,
        signature=signature_header,
        secret=settings.webhook_secret,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature",
        )

    return body


@router.post("/github")
async def handle_github_webhook(
    request: Request,
    body: Annotated[bytes, Depends(verify_webhook_signature)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    """Handle incoming GitHub webhook events.

    This endpoint receives and processes GitHub webhook events,
    performing HMAC verification and event triage.

    Args:
        request: The FastAPI request object.
        body: The verified raw request body.
        settings: Application settings.

    Returns:
        A confirmation message.
    """
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    delivery_id = request.headers.get("X-GitHub-Delivery", "unknown")

    logger.info(
        "Received webhook event: type=%s, delivery_id=%s",
        event_type,
        delivery_id,
    )

    # TODO: Implement event triage and queue initialization
    # - Parse issue body/labels
    # - Map to WorkItem objects
    # - Apply agent:queued label

    return {
        "status": "received",
        "event_type": event_type,
        "delivery_id": delivery_id,
    }


@router.get("/health")
async def webhook_health() -> dict[str, str]:
    """Health check endpoint for the webhook service."""
    return {"status": "healthy", "service": "webhooks"}
