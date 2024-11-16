"""Server module for the ssp package. Implements the main program logic."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._bot import TelegramBot
from ._webhook import GitHubWebhookHandler

if TYPE_CHECKING:
    from schemas import BlogData, PostConfigs, WebhookData


class Server:
    def __init__(
        self,
        webhook_data: WebhookData,
    ) -> None:
        """Initialize the Server.

        Args:
            bot (TelegramBot): The Telegram bot instance.
            webhook_data (WebhookData): The GitHub webhook handler instance.

        """
        self.__bot: TelegramBot
        self.__webhook_data = webhook_data

    async def __create_post(self, post_name: str, post_title: str) -> None:
        """Create a post and send it to the configured Telegram channels.

        Args:
            post_name (str): Name of the post to send.
            post_title (str): Title of the post to send.

        """
        await self.__bot.send_post(post_name=post_name, post_title=post_title)

    def setup_bot(
        self,
        blog_data: BlogData,
        post_configs: PostConfigs,
        token: str,
    ) -> None:
        """Set up the Telegram bot with the provided configuration.

        Args:
            blog_data (BlogData): The blog data to use for sending posts.
            post_configs (PostConfigs): The post configuration to use for sending posts.
            token (str): The Telegram bot token from @BotFather.

        """
        self.__bot = TelegramBot(
            token=token,
            post_configs=post_configs,
            blog_data=blog_data,
        )

    def get_webhook_handler(self) -> GitHubWebhookHandler:
        """Return the GitHub webhook handler instance.

        This method is used to create the webhook handler from the provided
        webhook data.

        Returns:
            GitHubWebhookHandler: The GitHub webhook handler instance.

        """
        return GitHubWebhookHandler(
            callback=self.__create_post,
            secret_token=self.__webhook_data.secret_token,
        )
