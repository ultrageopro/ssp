from dataclasses import dataclass


@dataclass(frozen=True)
class BlogData:
    blog_url: str
    blog_owner_name: str
