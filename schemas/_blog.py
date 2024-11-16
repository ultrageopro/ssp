from dataclasses import dataclass


@dataclass(frozen=True)
class BlogData:
    """Dataclass containing the blog data."""

    blog_url: str
    blog_owner_name: str
