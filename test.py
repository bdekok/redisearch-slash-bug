import os
from redis_om import (
    Field,
    HashModel,
    Migrator
)
from redis_om.connections import get_redis_connection
import logging

logging.getLogger().setLevel(logging.DEBUG)


class Page(HashModel):
    page_title: str = Field(index=True)
    url: str = Field(index=True)

    class Meta:
        host = os.environ.get('REDIS_HOST', 'localhost')
        database = get_redis_connection(
            url=f'redis://{host}:6379', decode_responses=True
        )


not_working = Page(
    page_title="Redis-OM Tutorial",
    url="www.youtube.com/watch?v=dQw4w9WgXcQ"
)
working = Page(
    page_title="Youtube homepage",
    url="www.youtube.com"
)
not_working.save()
working.save()

Migrator().run()
not_found = Page.find(Page.url == "www.youtube.com/watch?v=dQw4w9WgXcQ").all()
found = Page.find(Page.url == "www.youtube.com").all()
# When setting a breakpoint in redis_om/model/model.py thios translates to
# ft.search :__main__.Page:index @url:{www\\.youtube\\.com/watch?v\\=dQw4w9WgXcQ}
# ft.search :__main__.Page:index @url:{www\\.youtube\\.com}

logging.debug(f"Searching 'www.youtube.com/watch?v=dQw4w9WgXcQ' found {len(not_found)} records, value: {not_found}")
logging.debug(f"Searching www.youtube.com, found {len(found)} records, value: {found}")

