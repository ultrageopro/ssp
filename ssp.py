"""Main module for the ssp package. Executes the main function."""

from __future__ import annotations

import logging
from pathlib import Path

import tomllib
from asgiref.wsgi import WsgiToAsgi
from flask import Blueprint, Flask

from modules import Server
from schemas import BlogData, PostConfigs, WebhookData

# Setup logging
logging.basicConfig(level=logging.INFO)


def __load_blueprint(
    webhook_data: WebhookData,
    blog_data: BlogData,
    post_configs: PostConfigs,
    token: str,
) -> Blueprint:
    """Start the server.

    This function creates the server and sets up the telegram bot in it.
    The webhook blueprint is registered in the app and returned.

    Args:
        webhook_data (WebhookData): The webhook data.
        blog_data (BlogData): The blog data.
        post_configs (PostConfigs): The post configuration.
        token (str): The telegram bot token.

    Returns:
        Blueprint: The webhook blueprint.

    """
    # Create the server and set up telegram bot in it
    server = Server(webhook_data=webhook_data)
    server.setup_bot(blog_data=blog_data, post_configs=post_configs, token=token)

    # Get the webhook handler
    webhook = server.get_webhook_handler()
    return webhook.blueprint


# Load configuration data at the module level
with Path("config.toml").open("rb") as f:
    config_data = tomllib.load(f)

# Create instances
blog_data = BlogData(**config_data["blog"])
post_configs = PostConfigs(**config_data["telegram_channel"])
webhook_data = WebhookData(**config_data["webhook"])
token = config_data["bot"]["telegram_bot_token"]

# Start the server and create the blueprint
blueprint = __load_blueprint(
    webhook_data=webhook_data,
    blog_data=blog_data,
    post_configs=post_configs,
    token=token,
)

# Create the Flask app at the module level
app = Flask(__name__)
app.register_blueprint(blueprint)

# Convert the Flask app to an ASGI app
asgi_app = WsgiToAsgi(app)  # type: ignore[no-untyped-call]
