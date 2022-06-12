import click
from react_reminder import bot
from react_reminder import scheduler
import logging


@click.command()
@click.option("--redis_host", envvar="REDIS_HOST", type=str, required=True)
@click.option("--redis_port", envvar="REDIS_PORT", type=int, required=True)
@click.option("--redis_user", envvar="REDIS_USER", type=str, required=True)
@click.option("--redis_pass", envvar="REDIS_PASS", type=str, required=True)
@click.option("--redis_dbno", envvar="REDIS_DBNO", type=int, default=0)
@click.option(
    "--discord_bot_token", envvar="DISCORD_BOT_TOKEN", type=str, required=True
)
def run(
    redis_host: str,
    redis_port: int,
    redis_user: str,
    redis_pass: str,
    redis_dbno: int,
    discord_bot_token: str,
):
    logging.basicConfig(
        level=logging.DEBUG,
        encoding="utf-8",
        style="{",
        format="{levelname} {pathname} {funcName} {message}",
    )

    sched = scheduler.MakeScheduler(
        host=redis_host,
        port=redis_port,
        username=redis_user,
        db=redis_dbno,
        password=redis_pass,
    )

    client = bot.GetClient(scheduler=sched)
    client.run(discord_bot_token)


if __name__ == "__main__":
    run()
