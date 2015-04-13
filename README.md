# Crypt of the NecroDancer Unofficial Level Translator
Who wants to manually delete the default level and then place hundreds of wall and floor tiles just to make the basic structure of a CotND level? Nobody? Weird.

This is NOT supposed to be a full-fledged replacement level editor. Instead, this program translates levels from my own, custom format into the game's XML format. I think you'll find that my custom format is MUCH easier to work with, especially since you can use you favorite text editor to do it. (I recommend [Sublime Text 3](http://www.sublimetext.com/) for anyone who isn't already using anything that's more powerful, like emacs or vim)

I imagine this translator will mostly be used to create the basic structure of levels, after which you'll go into the in-game editor to make adjustments. But you certainly can develop entire dungeons using this program if you find it useful.

## How to use:

You need a dungeon file and one or more level files. (These can all be text files)

The dungeon file is in this format, where `$` represents a placeholder that you need to fill in:

    [settings]
        save_location = $
        name = $
        player_glyph = $
        floor_glyph = $
        character = $
        levels = $

    [tiles]
        $

    [enemies]
        $

    [items]
        $

    [chests]
        $

    [crates]
        $

    [shrines]
        $

    [database]
        $

I can't think of a good way to clearly explain in words what each of these `$`'s need to be replaced by, so please look at the files in the `./example` directory to see how things work; it should be pretty self-explanatory. **You may have to change the `save_location` key in the `[settings]` sections**

Run the example from the commandline as follows:

    $ cd example
    $ python3 ../necro_level_editor_helper.py dungeon.txt

(You must be in the folder that has your dungeon and level files in it when you run the translator)

## faq:

**Q:** How do I define tiles/enemies/items/etc?

**A:** Add a new line under the `[database]` heading in your dungeon file. This line will look something like this:

    green_skeleton = <enemy beatDelay="1" lord="0" type="4" x="{x}" y="{y}"></enemy>

Basically, you say `name = xml`, where `name` is a user-friendly name and `xml` is the XML that corresponds to it. **Make sure you include the closing XML tag!!** (in this case, `</enemy>`) The xml should also have two position placeholders: `x="{x}" y="{y}"`.

To define a glyph that corresponds to a green skeleton, add a new line under the `[enemies]` section, like this:

    g = ${database:green_skeleton}

Then, in your actual level file, type a `g` wherever you want to place a green skeleton

**Q:** How do I find the XML that corresponds to the various enemies/items/etc in the game?

**A:** You have to make a level using the in-game editor, place the type of object you want, save the level, and then examine the game's saved data, which should be located at `C:\Program Files (x86)\Steam\steamapps\common\Crypt of the NecroDancer\dungeons\MY DUNGEON.xml` (for windows users)

Sorry; I know it's a little awkward. As you build many dungeons over time, you should keep your old `[database]` settings, gradually adding new objects to your database as you need them. The example dungeon in `./example/dungeon.txt` has a very basic database already; I may expand this over time if I get around to it. (Pull requests are welcome!)

**Q:** Can I place multiple things in a single space?

**A:** Yes! You can place multiple things *of different types* in one space. For example, you can place an enemy, an item, and a floor tile all in a single space, but you can't place multiple enemies or multiple items on a single space. You do this by defining a glyph in multiple different sections. For example, assuming you have the XML for `green_skeleton`, `ice`, and `winged_boots` in your `[database]` section, you can create a glyph `x` that will be converted into a green skeleton that is standing on ice and winged boots with the following:

    [tiles]
        x = ${database:ice}
    [enemies]
        x = ${database:green_skeleton}
    [items]
        x = ${database:winged_boots}

**Q:** I used this tool and generated an XML dungeon. When I tried to load it in-game, my game crashed. Help!

**A:** That's not technically a question, but I'll humor you. One easy mistake to make is to forget to close the XML tags that you've defined in your `[database]` section. I'm working on a feature that will warn you about this.

If that doesn't fix it, then I'm sorry. Please let me know so that I can fix any bugs that might be in my translator! You can create an issue here on github or you can email me at pancelor@gmail.com.

### Happy level editing!

To make your mouth water a little, the following is the exact text of `example/level1.txt`:

    +x+++x+++x+
    x++//////+x
    ++/////c//+
    +/////////+
    +///p////++
    x///////++x
    +/+/////+/+
    +////+//+/+
    +/////c//s+
    +/+/////+/+
    x///+///+/x
    +x+++x+++x+

Building that text file in a moderately powerful text editor is *much* easier than using the in-game level editor.