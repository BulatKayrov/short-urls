import unittest

from api.v1.short_url.schemas import SCreateShortUrl, ShortUrl  # type: ignore


class ShortUrlCreateTestCase(unittest.TestCase):

    def test_short_url_create(self) -> None:  # type: ignore
        short_url_in = SCreateShortUrl(
            slug="short-url",
            target_url="https://example.com",
            description="default",
        )

        short_url = ShortUrl(**short_url_in.model_dump())

        self.assertEqual(short_url.target_url, short_url_in.target_url)
        self.assertEqual(short_url.description, short_url_in.description)
        self.assertEqual(short_url.slug, short_url_in.slug)
