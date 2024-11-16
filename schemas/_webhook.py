from dataclasses import dataclass


@dataclass(frozen=True)
class WebhookData:
    """Dataclass containing webhook data."""

    secret_token: str
    commit_template: str
