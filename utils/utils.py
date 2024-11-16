"""Utility functions for the ssp package represented in Utils class."""

from __future__ import annotations

import hmac
import re
from hashlib import sha256


class Utils:
    @staticmethod
    def get_post_from_template(post_template: str, **kwargs: str) -> str:
        """Return a post from a template.

        Args:
            post_template (str): The template to use.
            **kwargs: Keyword arguments to replace in the template.
            Defaults are (str): blog_owner_name, blog_url, post_name, post_title

        Returns:
            str: The post as a string.

        """
        return post_template.format(**kwargs)

    @staticmethod
    def parse_commit(
        commit_message: str,
        commit_template: str,
    ) -> tuple[str, str] | None:
        """Extract `post_name` and `post_title` from a commit message based on the commit template.

        Args:
            commit_message (str): The commit message text.
            commit_template (str): The commit template to use, which contains placeholders like <post_name> and <post_title>.

        Returns:
            Optional[Tuple[str, str]]: A tuple containing `post_name` and `post_title`, or None if the format does not match.

        """  # noqa: E501
        # Escape special characters in the template except placeholders
        regex_pattern = re.escape(commit_template)

        # Replace placeholders with regex patterns that match content inside <>
        regex_pattern = regex_pattern.replace(
            re.escape("<post_name>"),
            r"(?P<post_name>.+?)",
        )
        regex_pattern = regex_pattern.replace(
            re.escape("<post_title>"),
            r"(?P<post_title>.+?)",
        )

        # Match the regex against the commit message
        match = re.fullmatch(regex_pattern, commit_message)

        if not match:
            return None

        # Extract the values of `post_name` and `post_title`
        try:
            post_name = match.group("post_name").strip(" <>")
            post_title = match.group("post_title").strip(" <>")
        except IndexError:
            return None
        else:
            return post_name, post_title

    @staticmethod
    def verify_signature(
        body: bytes,
        secret_token: str,
        recieved_signature: str,
    ) -> bool:
        """Verify the HMAC SHA-256 signature of a given payload.

        Args:
            body (bytes): The request body payload.
            secret_token (str): The secret token used to generate the HMAC signature.
            recieved_signature (str): The signature received from the request headers.

        Returns:
            bool: True if the computed signature matches the received signature, False otherwise.

        """  # noqa: E501
        hash_object = hmac.new(
            key=bytes(secret_token, "utf-8"),
            msg=body,
            digestmod=sha256,
        )
        expected_sign = f"sha256={hash_object.hexdigest()}"

        return hmac.compare_digest(expected_sign, recieved_signature)
