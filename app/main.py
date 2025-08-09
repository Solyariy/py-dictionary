from __future__ import annotations
from collections import namedtuple
from collections.abc import Hashable
from typing import Any

Node = namedtuple("Node", ["key", "hash", "value"])


class Dictionary:
    def __init__(self) -> None:
        self.storage: list[Node] = [None] * 8
        self.length = 0
        self.capacity = 8

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        current = self.storage[index]
        if current is None:
            return
        while self.storage[index].key != key:
            index = (index + 1) % self.capacity
            if self.storage[index] is None:
                return
        self.storage[index] = None

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        current = self.storage[index]
        if current is None:
            raise KeyError("Missing key")
        while self.storage[index].key != key:
            index = (index + 1) % self.capacity
            if self.storage[index] is None:
                raise KeyError("Missing key")
        return self.storage[index].value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.need_resize():
            self.resize()
        hash_ = hash(key)
        index = hash_ % self.capacity
        node = Node(
            key=key,
            hash=hash_,
            value=value
        )
        self.__set_item(node, index)

    def __set_item(self, node: Node, index: int) -> None:
        while True:
            if self.storage[index] is None:
                self.storage[index] = node
                self.length += 1
                break
            if self.storage[index].key == node.key:
                self.storage[index] = node
                break
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def need_resize(self) -> bool:
        return self.length >= self.capacity * 2 // 3

    def resize(self) -> None:
        self.capacity *= 2
        old_storage = self.storage
        self.storage = [None] * self.capacity
        self.length = 0
        for item in old_storage:
            if not item:
                continue
            index = item.hash % self.capacity
            self.__set_item(item, index)

    def clear(self) -> None:
        self.storage = [None] * 8
        self.capacity = 8
        self.length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        value = self.get(key, default)
        if value == default:
            raise KeyError("Missing key")
        del self[key]
        return value

    def update(self, data: dict[Any, Any] | Dictionary) -> None:
        for key in data:
            self[key] = data[key]

    def __iter__(self) -> Dictionary:
        for node in self.storage:
            if node:
                yield node.key
