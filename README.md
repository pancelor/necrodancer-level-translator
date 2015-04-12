# necrodancer-level-editor
Who wants to manually delete the default level and then place hundreds of wall and floor tiles just to make the basic structure of a CotND level? Nobody? Weird. 

This is NOT supposed to be a full-fledged replacement editor. I imagine it will be mostly used to create the basic structure of levels, after which you'll go into the in-game editor to make adjustments. It's not particularly user friendly; I made it for myself because the in-game editor can be quite clunky.

## faq:

**Q:** How do I define tiles/enemies/items/etc?

**A:** Add a new line under the `[database]` heading in your dungeon file. This line will look something like this:

    green_skeleton = <enemy beatDelay="1" lord="0" type="4" x="{x}" y="{y}"></enemy>
    
Basically, you say 'name = xml', where name is a user-friendly name and xml is the xml that corresponds to it. **Make sure you include the closing XML tag!!** (in this case, '</enemy>') The xml should have two position placeholders: `x="{x}" y="{y}"`.

Then, up under the `[enemies]` heading, to define a glyph that corresponds to a green skeleton, make a new line like this:

    g = ${database:green_skeleton}
    
Then, in your actual level file, type a `g` whereever you want to place a green skeleton

**Q:** Can I place multiple things in a single space?




Run it from the commandline as follows:

    $ python3 necro_level_editor_helper.py example/ice.txt
