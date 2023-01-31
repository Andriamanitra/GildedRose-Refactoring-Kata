from hypothesis import given
import hypothesis.strategies as st

from gilded_rose import Item, GildedRose

MAX_QUALITY = 50
qualities = st.integers(min_value=0, max_value=MAX_QUALITY)
nonlegendary_item_types = st.sampled_from([
    "Aged Brie",
    "Backstage passes to a TAFKAL80ETC concert",
    "Conjured",
    "other"
])

@given(
    nonlegendary_item_types, st.integers(), qualities,
    nonlegendary_item_types, st.integers(), qualities,
)
def test_nonlegendary_items_sell_by_date_decreases(
        itemtype1, sell_in1, quality1,
        itemtype2, sell_in2, quality2
):
    item1 = Item(itemtype1, sell_in1, quality1)
    item2 = Item(itemtype2, sell_in2, quality2)
    gilded_rose = GildedRose([item1, item2])
    gilded_rose.update_quality()
    assert item1.sell_in == sell_in1 - 1
    assert item2.sell_in == sell_in2 - 1

@given(st.integers(min_value=1), qualities)
def test_aged_brie_before_expiration(sell_in, quality):
    item = Item("Aged Brie", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == min(MAX_QUALITY, quality + 1)

@given(st.integers(max_value=0), qualities)
def test_aged_brie_after_expiration(sell_in, quality):
    item = Item("Aged Brie", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == min(MAX_QUALITY, quality + 2)

@given(st.integers())
def test_sulfuras_never_changes(sell_in):
    item = Item("Sulfuras, Hand of Ragnaros", sell_in, 80)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == 80
    assert item.sell_in == sell_in

@given(st.integers(min_value=11), qualities)
def test_backstage_passes_over_10_days(sell_in, quality):
    item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == min(MAX_QUALITY, quality + 1)

@given(st.integers(min_value=6, max_value=10), qualities)
def test_backstage_passes_under_10_days(sell_in, quality):
    item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == min(MAX_QUALITY, quality + 2)

@given(st.integers(min_value=1, max_value=5), qualities)
def test_backstage_passes_under_5_days(sell_in, quality):
    item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == min(MAX_QUALITY, quality + 3)

@given(st.integers(max_value=0), qualities)
def test_backstage_passes_zero_after_concert(sell_in, quality):
    item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == 0

@given(st.integers(min_value=1), qualities)
def test_other_items_lose_quality_before_expiration(sell_in, quality):
    item = Item("other", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == max(0, quality - 1)

@given(st.integers(max_value=0), qualities)
def test_other_items_lose_2_quality_after_expiration(sell_in, quality):
    item = Item("other", sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == max(0, quality - 2)
