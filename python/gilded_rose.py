# -*- coding: utf-8 -*-


class BaseItem:
    def __init__(self, item):
        self.max_quality = 50
        self.item = item

    @property
    def expired(self):
        return self.item.sell_in <= 0

    def update_quality(self, change=-1):
        if self.expired:
            quality = self.item.quality + 2 * change
        else:
            quality = self.item.quality + change
        self.item.quality = min(self.max_quality, max(0, quality))
        self.item.sell_in -= 1


class Legendary(BaseItem):
    def update_quality(self):
        pass


class AgedBrie(BaseItem):
    def update_quality(self):
        super().update_quality(+1)


class BackstagePass(BaseItem):
    def update_quality(self):
        if self.expired:
            self.item.quality = 0
            super().update_quality(0)
        elif self.item.sell_in < 6:
            super().update_quality(+3)
        elif self.item.sell_in < 11:
            super().update_quality(+2)
        else:
            super().update_quality(+1)


class GildedRose(object):
    def __init__(self, items):
        self.items = []
        for item in items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                new_item = Legendary(item)
            elif item.name == "Aged Brie":
                new_item = AgedBrie(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                new_item = BackstagePass(item)
            else:
                new_item = BaseItem(item)
            self.items.append(new_item)

    def update_quality(self):
        for item in self.items:
            item.update_quality()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
