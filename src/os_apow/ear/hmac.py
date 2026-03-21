"""HMAC signature verification for GitHub webhooks.

This module provides cryptographic verification functions to prevent webhook spoofing.
"""

import hashlib
import hmac
from typing import Final

# GitHub uses HMAC-SHA256 for webhook signatures
HASH_ALGORITHM: Final = "sha256"
SIGNATURE_PREFIX: Final = "sha256="


def verify_github_signature(
    body: bytes,
    signature: str,
    secret: str,
) -> bool:
    """Verify the HMAC-SHA256 signature of a GitHub webhook payload.

    Args:
        body: The raw request body bytes.
        signature: The X-Hub-Signature-256 header value (e.g., "sha256=...").
        secret: The webhook secret configured in GitHub.

    Returns:
        True if the signature is valid, False otherwise.
    """
    if not signature.startswith(SIGNATURE_PREFIX):
        return False

    # Extract the hex digest from the signature
    expected_sig = signature[len(SIGNATURE_PREFIX) :]

    # Compute the HMAC-SHA256 digest
    computed_sig = hmac.new(
        key=secret.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_sig, expected_sig)


def compute_signature(body: bytes, secret: str) -> str:
    """Compute the HMAC-SHA256 signature for a payload.

    This is useful for testing webhook handlers.

    Args:
        body: The raw request body bytes.
        secret: The webhook secret.

    Returns:
        The signature string in the format "sha256=...".
    """
    digest = hmac.new(
        key=secret.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return f"{SIGNATURE_PREFIX}{digest}"
