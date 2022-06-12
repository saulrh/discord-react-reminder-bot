import apscheduler.schedulers.asyncio
import apscheduler.schedulers.base
import apscheduler.jobstores.redis


def MakeScheduler(*args, **kwargs) -> apscheduler.schedulers.base.BaseScheduler:
    jobstores = {"default": apscheduler.jobstores.redis.RedisJobStore(*args, **kwargs)}
    scheduler = apscheduler.schedulers.asyncio.AsyncIOScheduler(jobstores=jobstores)
    scheduler.start()
    return scheduler
