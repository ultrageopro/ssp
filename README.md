# Super Shit Post (SSP)

## Automatic Article Posting from My Website to My Telegram Channel

This project automates the process of posting articles from [**MY website**](https://site.ultrageopro.ru) (blog section) to **MY Telegram channel**. All styles, message formatting, and commit checks are specifically written for my use case. However, I have made it as customizable as possible so that anyone who wishes to use the code can easily configure links and formatting through the project's configuration files.

## Instructions
**First**, it's important to understand how the program works: it operates through a **webhook attached to your website's repository** (on GitHub). As soon as you make a commit with a new blog (the commit message must follow the format specified in the _configs_), the server receives the title and heading of the article and sends the post (in the specified format) **to all the IDs listed in the configs**.

All other instructions for filling out and the program's logic can be found in the comments within the `config file`.

## Configuration File (`config.toml`)

`required` fields - you **must** fill/change them.

`optional` fields - you may leave them without any changes.

```toml
[blog]
blog_url = "https://site.ultrageopro.ru/blog" # str[required]: Blog url
blog_owner_name = "ultrageopro" # str[required]: Blog owner name, one word

[bot]
telegram_bot_token = "" # str[required]: Telegram bot token from @BotFather

[webhook]
secret_token = "" # str[required]: Secret for webhook

# str[optional]: Commit template.
# post_name must be only one word without spaces (use - instead of spaces), cus it will be used in a link to the post
# post_title can contain spaces
# Example of commit: "post: <hello-world> <Hello World!>"
commit_template = "post: <post_name> <post_title>"

[telegram_channel]

# list[int][optional]: Telegram channel ids, where to send posts
channel_ids = []

# str[optional]: Post template
# You can leave it without any changes
# {blog_owner_name} {blog_url} {post_name} {post_title} will be replaced with actual values
post_template = """
New post from [{blog_owner_name}'s blog]({blog_url})!

*{post_title}*
[Read more]({blog_url}/{post_name})

This post was automatically created with [SSP](https://github.com/ultrageopro/ssp)
"""
```

## Deployment and Usage
After setting up the application in `config.toml`:

1. Deploy the application somewhere. For example, I would recommend using [fly.io](https://fly.io)
   1. Create an account and install `flyctl`.
   2. Log in to your account using `fly auth login` and launch the application (from the main directory) with `fly launch`.
   3. After a successful launch, the webhook will be listening at the address `https://example.fly.io/webhook`. The domain will be provided in the console output after a successful launch.

2. [Create a webhook](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks) in your website's repository:
   1. Paste the address obtained in step 1.3. **Be sure** to enter the secret that was specified in `config.toml`.
   2. Allow push notifications to be sent; all other notifications will be ignored.
   3. Choose the data type `application/json`.
   4. Create the webhook and check its operation in the "Recent Deliveries" section.

3. **That's it!**

## Author & License

This project was created by [**ultrageopro**](https://github.com/ultrageopro)

This project is released under the [MIT License](https://github.com/ultrageopro/ssp/blob/main/LICENSE)