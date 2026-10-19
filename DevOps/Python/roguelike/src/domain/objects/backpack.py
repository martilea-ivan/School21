from domain.objects.enum import ItemType, GenerationConfig

class Backpack:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    def add_item(self, item):
        if item.type == ItemType.TREASURE:
            for i in self._items:
                if i.type == ItemType.TREASURE:
                    i.gold += item.gold
                    return True
            self._items.append(item)
            return True

        count = sum(1 for x in self._items if x.type == item.type)
        if count >= GenerationConfig.MAX_ITEMS_PER_TYPE.value:
            return False
        self._items.append(item)
        return True

    def remove_item(self, item):
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def get_items_by_type(self, item_type):
        return [x for x in self._items if x.type == item_type]

    def to_dict(self):
        return {"items": [item.to_dict() for item in self._items]}