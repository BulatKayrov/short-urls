import uuid
from unittest import TestCase

from redis import Redis

from api.v1.short_url.crud import ShortUrlsStorage
from api.v1.short_url.schemas import SCreateShortUrl, SUpdatePartialShortUrl, ShortUrl
from core.config import settings

redis_test_short_url_storage = Redis(
    host=settings.TEST_REDIS_HOST,
    port=settings.TEST_REDIS_PORT,
    db=settings.TEST_REDIS_SHORT_URL,
    decode_responses=True,
)

storage = ShortUrlsStorage(helper=redis_test_short_url_storage)


class ShortUrlServiceTestCase(TestCase):

    def setUp(self):
        self.short_url = self.create_short_url()

    def create_short_url(self) -> ShortUrl:
        short_url_in = SCreateShortUrl(
            target_url="https://example.com", slug=uuid.uuid4().hex[:10]
        )
        return storage.create(data=short_url_in)

    def tearDown(self):
        storage.delete_short_url(self.short_url)

    def test_short_url_update(self):
        old_description = self.short_url.description

        short_url_update = SUpdatePartialShortUrl(**self.short_url.model_dump())
        short_url_update.description = "new description"
        updated_short_url = storage.update_short(
            short_url=self.short_url, short_url_in=short_url_update
        )

        self.assertNotEqual(old_description, updated_short_url.description)
        self.assertEqual(short_url_update.description, updated_short_url.description)

    def test_short_partial_url_update(self):
        new_url = "https://yoyo.com/"
        short_url_in = SUpdatePartialShortUrl(target_url=new_url)
        new_short_url = storage.update_short(
            short_url=self.short_url, short_url_in=short_url_in, partial=True
        )

        self.assertEqual(new_url, new_short_url.target_url.encoded_string())
