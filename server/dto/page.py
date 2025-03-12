from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: list[T]
    total_items: int
    total_pages: int
    current_page: int

    def to_dict(self, item_serializer=None):
        items = (
            item_serializer.dump(self.items, many=True)
            if item_serializer
            else self.items
        )
        return {
            "items": items,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "current_page": self.current_page,
        }
