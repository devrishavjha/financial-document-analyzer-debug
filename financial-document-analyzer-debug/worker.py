import os

import redis
from rq import Connection, Queue, Worker


def main() -> None:
    """
    Start an RQ worker that processes financial analysis jobs.

    The worker listens on the 'financial_analysis' queue and uses REDIS_URL
    (default: redis://localhost:6379/0) to connect to Redis.
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    conn = redis.from_url(redis_url)

    listen_queues = ["financial_analysis"]

    with Connection(conn):
        worker = Worker([Queue(name) for name in listen_queues])
        worker.work()


if __name__ == "__main__":
    main()

