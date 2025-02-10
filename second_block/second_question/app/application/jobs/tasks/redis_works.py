from dishka.integrations.taskiq import inject, FromDishka
from redis.asyncio import Redis

from app.application.jobs.main import broker


@broker.task(
    schedule=[
        {
            "cron": "11 14 * * *"
        }
    ]
)
@inject
async def clear_redis(redis: FromDishka[Redis]) -> None:
    await redis.flushdb(asynchronous=True)
