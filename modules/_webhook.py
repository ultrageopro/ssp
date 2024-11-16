from __future__ import annotations

import logging
from typing import Any, Callable, Coroutine

from flask import Blueprint, Response, abort, jsonify, request

from utils import Utils


class GitHubWebhookHandler:
    def __init__(
        self,
        secret_token: str,
        callback: Callable[[str], Coroutine[Any, Any, None]],
    ) -> None:
        """Initialize the GitHubWebhookHandler.

        Args:
            secret_token (str): The secret token of the webhook.
            callback (Callable[[list[str]], Couroutine[Any, Any, None]]): The callback to call with the commit messages.

        """  # noqa: E501
        self.__secret_token = secret_token
        self.__callback = callback
        self.__blueprint = Blueprint("webhook", __name__)
        self.__blueprint.add_url_rule(
            "/webhook",
            view_func=self.handle_webhook,
            methods=["POST"],
        )
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)

    async def handle_webhook(self) -> tuple[Response, int]:
        """Handle incoming GitHub webhook requests.

        Verifies the request signature and processes the event if it is a 'push' event.
        Extracts commit messages from the payload for further processing.

        Returns:
            tuple[int, str]: A tuple containing the HTTP status code and a JSON response.
                The JSON response includes the status and either the commit messages or a
                reason for ignoring the event.

        """  # noqa: E501
        signature = request.headers.get("X-Hub-Signature-256")
        if signature is None:
            self.__logger.error("Missing X-Hub-Signature-256 header")
            abort(400, "Missing X-Hub-Signature-256")

        valid = Utils.verify_signature(
            body=request.data,
            recieved_signature=signature,
            secret_token=self.__secret_token,
        )
        if not valid:
            self.__logger.error("Invalid signature")
            abort(400, "Invalid signature")

        self.__logger.info("Signature verified!")

        event = request.headers.get("X-GitHub-Event")
        if event == "push":
            payload: dict[str, Any] | None = request.json
            if payload is None:
                self.__logger.error("Invalid payload: Payload is None")
                abort(400, "Invalid payload")

            commit_message = payload.get("head_commit", {}).get("message")
            if commit_message is None:
                self.__logger.error("Invalid payload: Commit message is None")
                abort(400, "Invalid payload")

            self.__logger.info(
                "Push event received with commit message: %s",
                commit_message,
            )

            # Execute the callback with commit messages
            await self.__callback(commit_message)
            return jsonify({"status": "success", "message": commit_message}), 200

        self.__logger.info("Event ignored: %s", event)
        return (
            jsonify({"status": "ignored", "reason": "Not a push event"}),
            200,
        )

    @property
    def blueprint(self) -> Blueprint:
        """Return the Flask Blueprint for the webhook.

        Returns:
            Blueprint: The Flask Blueprint for the webhook.

        """
        return self.__blueprint
