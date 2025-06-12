import uuid
from typing import ClassVar
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


def create_short_url(target_url="https://example.com") -> ShortUrl:
    short_url_in = SCreateShortUrl(target_url=target_url, slug=uuid.uuid4().hex[:10])
    return storage.create(data=short_url_in)


class ShortUrlServiceTestCase(TestCase):

    def setUp(self):
        self.short_url = create_short_url()

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


class ShortUrlMethodsGetTestCase(TestCase):
    SHORT_URLS_COUNT = 3
    short_urls: ClassVar[list[ShortUrl]] = []

    @classmethod
    def setUpClass(cls):
        cls.short_urls = [create_short_url() for _ in range(cls.SHORT_URLS_COUNT)]

    @classmethod
    def tearDownClass(cls):
        for short_url in cls.short_urls:
            storage.delete_short_url(short_url)

    def test_get_short_url_by_slug(self):
        expected_slug = [_ for _ in self.short_urls][0].slug
        get_value = storage.get_by_slug(expected_slug)
        short_url = [_ for _ in self.short_urls if _.slug == expected_slug][0]
        self.assertEqual(short_url, ShortUrl.model_validate_json(get_value))

    def test_get_list(self):
        values = [_.slug for _ in storage.get()]
        expected_slug = [_.slug for _ in self.short_urls]

        self.assertEqual(len(expected_slug), len(values))
        self.assertIsNotNone(values)
        self.assertIn(expected_slug[0], values)
