from pydantic import BaseModel, AnyHttpUrl, Field


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: str | None = "default"


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенных ссылок
    """

    slug: str


class SCreateShortUrl(ShortUrlBase):
    """
    Модель создания записи
    """

    # slug: Annotated[str, Len(min_length=5, max_length=1000)]
    slug: str = Field(..., min_length=6, max_length=1000, examples=["example"])


class SUpdateShortUrl(ShortUrlBase):
    target_url: AnyHttpUrl
    description: str | None = "default"


class SUpdatePathShortUrl(ShortUrlBase):
    target_url: AnyHttpUrl | None = None
    description: str | None = None


class ShortUrlFroAdmin(ShortUrl):
    visits: int = 40
