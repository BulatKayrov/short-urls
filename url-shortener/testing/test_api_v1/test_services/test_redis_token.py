import unittest
from os import getenv

from api.v1.short_url.auth.service.redis_tokens import RedisTokenHelper
from core.config import settings

if getenv("TESTING") != "1":
    raise EnvironmentError("Must be run in testing mode")

redis_test_service = RedisTokenHelper(
    host=settings.TEST_REDIS_HOST,
    port=settings.TEST_REDIS_PORT,
    redis_db=settings.TEST_REDIS_DB,
    tokens_set_name=settings.TEST_TOKENS_SET_NAME,
)


class RedisTokenServicesTestCase(unittest.TestCase):

    def test_generate_and_save(self):
        token = redis_test_service.generate_token_and_save()
        self.assertIsNotNone(token)
        expected_exists = redis_test_service.token_exists(token)
        self.assertEqual(first=expected_exists, second=True)
