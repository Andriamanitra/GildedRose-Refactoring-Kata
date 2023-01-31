# -*- coding: utf-8 -*-

class GildedRose(object):
    def __init__(self, items):
        self.items = items

    @staticmethod
    def update_item_quality(item, quality_change):
        if quality_change < 0:
            item.quality = max(0, item.quality + quality_change)
        else:
            item.quality = min(50, item.quality + quality_change)

    def update_quality(self):
        for item in self.items:
            expired = item.sell_in <= 0

            if item.name == "Sulfuras, Hand of Ragnaros":
                continue
            elif item.name == "Aged Brie":
                self.update_item_quality(item, +2 if expired else +1)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                if expired:
                    item.quality = 0
                elif item.sell_in >= 11:
                    self.update_item_quality(item, +1)
                elif item.sell_in >= 6:
                    self.update_item_quality(item, +2)
                elif item.sell_in > 0:
                    self.update_item_quality(item, +3)
            else:
                self.update_item_quality(item, -2 if expired else -1)
            item.sell_in -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
