# necrodancer-level-translator
Who wants to manually delete the default level and then place hundreds of wall and floor tiles just to make the basic structure of a CotND level? Nobody? Weird. 

This is NOT supposed to be a full-fledged replacement editor. I imagine it will be mostly used to create the basic structure of levels, after which you'll go into the in-game editor to make adjustments. It's not particularly user friendly; I made it for myself because the in-game editor can be quite clunky.

## faq:

**Q:** How do I define tiles/enemies/items/etc?

**A:** Add a new line under the `[database]` heading in your dungeon file. This line will look something like this:

    green_skeleton = <enemy beatDelay="1" lord="0" type="4" x="{x}" y="{y}"></enemy>
    
Basically, you say 'name = xml', where name is a user-friendly name and xml is the xml that corresponds to it. **Make sure you include the closing XML tag!!** (in this case, `</enemy>`) The xml should also have two position placeholders: `x="{x}" y="{y}"`.

Then, up under the `[enemies]` heading, to define a glyph that corresponds to a green skeleton, make a new line like this:

    g = ${database:green_skeleton}
    
Then, in your actual level file, type a `g` whereever you want to place a green skeleton

**Q:** Can I place multiple things in a single space?

**A:** Yes! You can place multiple thing *of different types* in one space. For example, you can place an enemy, an item, and a floor tile all in a single space, but you can't place multiple enemies or multiple items. You do this by defining a glyph in multiple different sections. For example, assuming you have the xml for `green_skeleton` and `ice` in your `[database]` section, you can create a glyph `x` that will be converted into a green skeleton standing on ice with the following:

    [tiles]
        x = ${database:ice}
    [enemies]
        x = ${database:green_skeleton}


Run it from the commandline as follows:

    $ cd example
    $ python3 ../necro_level_editor_helper.py ice.txt

(You must be in the folder that has your dungeon and level files in it when you run the translator)
