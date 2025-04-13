from pydantic import BaseModel, AnyHttpUrl, Field


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенных ссылок
    """


class SCreateShortUrl(ShortUrlBase):
    """
    Модель создания записи
    """

    # slug: Annotated[str, Len(min_length=5, max_length=1000)]
    slug: str = Field(..., min_length=6, max_length=1000, examples=["example"])
