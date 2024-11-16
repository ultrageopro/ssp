from __future__ import annotations

from typing import TYPE_CHECKING

from telebot.async_telebot import AsyncTeleBot
from telebot.async_telebot import logging as tb_logging
from telebot.asyncio_helper import ApiTelegramException

from utils import Utils

if TYPE_CHECKING:
    from schemas import BlogData, PostConfigs


class TelegramBot:
    def __init__(
        self,
        token: str,
        post_configs: PostConfigs,
        blog_data: BlogData,
    ) -> None:
        """Initialize TelegramBot instance with a token.

        Args:
            token (str): Telegram bot token from @BotFather.
            post_configs (PostConfigs): Post configurations.
            blog_data (BlogData): Blog data with blog url and blog owner name.

        """
        self.__post_configs = post_configs
        self.__blog_data = blog_data

        self.__bot = AsyncTeleBot(token)
        tb_logging.info("Telegram bot initialized!")

    async def send_post(self, post_name: str, post_title: str) -> None:
        """Send a post to specified Telegram channels.

        Args:
            channel_ids (list[int]): IDs of Telegram channels to send the post to.
            post_name (str): Name of the post to send (to create url like example.com/blog/{post_name}).
            post_title (str): Title of the post to send.

        """  # noqa: E501
        template = self.__post_configs.post_template

        # Get required data about blog
        author = self.__blog_data.blog_owner_name
        blog_url = self.__blog_data.blog_url

        # Generate post to send using post template from config
        post_text = Utils.get_post_from_template(
            template,
            blog_owner_name=author,
            blog_url=blog_url,
            post_name=post_name,
            post_title=post_title,
        )

        tb_logging.info("Sending post %s to channels", post_name)
        try:
            for channel_id in self.__post_configs.channel_ids:
                await self.__bot.send_message(
                    channel_id,
                    post_text,
                    parse_mode="Markdown",
                )
                tb_logging.info("Post %s sent to channel %s", post_name, channel_id)
        except ApiTelegramException as e:
            tb_logging.error(
                "Error occured: %s while sending post to channel %s",
                e,
                channel_id,
            )
        finally:
            # Close bot session, as it is not needed anymore
            # If you don't close it, there will be an error
            await self.__bot.close_session()
            tb_logging.info("Bot session closed.")
