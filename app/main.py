from __future__ import annotations
from collections import namedtuple
from collections.abc import Hashable
from copy import deepcopy
from typing import Any

Node = namedtuple("Node", ["key", "hash", "value"])


class Dictionary:
    def __init__(self) -> None:
        self.storage: list[Node] = [None] * 8
        self.length = 0
        self.capacity = 8

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        self.storage[index] = None

    def __getitem__(self, item: Hashable) -> Any:
        index = hash(item) % self.capacity
        current = self.storage[index]
        if not current:
            raise KeyError("Missing key")
        while current.key != item:
            index = (index + 1) % self.capacity
            current = self.storage[index]
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
        old_storage = deepcopy(self.storage)
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
        del self[key]
        return value

    def update(self, values: dict[Any, Any] | Dictionary) -> None:
        for key, value in values.items():
            self[key] = value

    def __iter__(self) -> Dictionary:
        self.counter = -1
        return self

    def __next__(self) -> Any:
        self.counter += 1
        if self.storage[self.counter] is not None:
            return self.storage[self.counter].key
        while self.counter < self.capacity:
            if self.storage[self.counter] is None:
                self.counter += 1
            else:
                return self.storage[self.counter].key
        raise StopIteration
