"""Dataclass containing the post template and list of channel ids."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PostConfigs:
    channel_ids: list[int]
    post_template: str
