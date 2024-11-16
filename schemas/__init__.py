"""All schemas for the ssp package."""

from schemas._blog import BlogData
from schemas._t_channel import PostConfigs
from schemas._webhook import WebhookData

__all__ = ["BlogData", "PostConfigs", "WebhookData"]
