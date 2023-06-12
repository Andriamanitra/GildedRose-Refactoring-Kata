import Base

mutable struct Item{T<:Integer}
    name::String
    sellin::T
    quality::T
end

abstract type AbstractItem end

struct RegularItem <: AbstractItem
    item::Item{Int64}
end

struct LegendaryItem <: AbstractItem
    item::Item{Int64}
end

Base.show(io::IO, x::Item) = print(io, "$(x.name), $(x.sellin), $(x.quality)")
Base.show(io::IO, x::AbstractItem) = Base.show(io, x.item)

struct GildedRose
    items
    function GildedRose(items)
        item_types = Dict("Sulfuras, Hand of Ragnaros" => LegendaryItem)
        make_item(x) = get(item_types, x.name, RegularItem)(x)
        new(make_item.(items))
    end
end

function update_quality!(::LegendaryItem)
    # Legendary items never change
end

function update_quality!(item::AbstractItem)
    update_quality!(item.item)
end

function update_quality!(item::Item, change)
    item.quality = clamp(item.quality + change, 0:50)
end

is_expired(item::Item) = item.sellin <= 0

function update_quality!(item::Item)
    if item.name == "Aged Brie"
        update_quality!(item, is_expired(item) ? +2 : +1)
    elseif item.name == "Backstage passes to a TAFKAL80ETC concert"
        update_quality!(item, +1)
        if item.name == "Backstage passes to a TAFKAL80ETC concert"
            if item.sellin < 11
                update_quality!(item, +1)
            end
            if item.sellin < 6
                update_quality!(item, +1)
            end
        end
        if is_expired(item)
            item.quality = 0
        end
    else
        update_quality!(item, is_expired(item) ? -2 : -1)
    end
    item.sellin -= 1
end

function update_quality!(gr::GildedRose)
    update_quality!.(gr.items)
    return nothing
end

# Technically, julia espouses a REPL-driven workflow, so the preferred way to run this
# would be from the REPL. However, if you'd like to run this function from the
# commandline, run `$ julia -e 'include("gilded_rose.jl"); main(;days=3)'` or whatever
# number you want for `days`.
function main(; days::Int64=2)
    println("OMGHAI!")
    items = [
        Item("+5 Dexterity Vest", 10, 20),
        Item("Aged Brie", 2, 0),
        Item("Elixir of the Mongoose", 5, 7),
        Item("Sulfuras, Hand of Ragnaros", 0, 80),
        Item("Sulfuras, Hand of Ragnaros", -1, 80),
        Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),
        Item("Backstage passes to a TAFKAL80ETC concert", 10, 49),
        Item("Backstage passes to a TAFKAL80ETC concert", 5, 49),
        Item("Conjured Mana Cake", 3, 6),
    ]
    for day in 0:days
        println("-------- day $day --------")
        println("name, sellIn, quality")
        for item in items
            println(item)
        end
        println()
        update_quality!(GildedRose(items))
    end
end
