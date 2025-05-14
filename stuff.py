from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    db=settings.REDIS_DB,
)


def main():
    print(redis.ping())
    redis.set(name="name", value="value")
    print(redis.get(name="name").decode())
    print(redis.keys())
    print(redis.get("yoyo"))
    redis.delete("name")


if __name__ == "__main__":
    main()
