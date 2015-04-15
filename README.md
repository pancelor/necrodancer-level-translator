# Crypt of the NecroDancer Unofficial Level Translator
Who wants to manually delete the default level and then place hundreds of wall and floor tiles just to make the basic structure of a CotND level? Nobody? Weird.

Instead, fire up your favorite text editor and design levels like this:

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

(this is the exact text of example/level1.txt)

This tool is NOT supposed to be a full-fledged replacement level editor. Instead, this program translates dungeons from my own, custom format into the game's XML format. I think you'll find that my custom format is much easier to work with, especially since you can use you favorite text editor to do it. (I recommend [Sublime Text 3](http://www.sublimetext.com/) for anyone who isn't already using anything that's more powerful, like emacs or vim. Being able to use multiple cursors is pretty great)

I imagine this translator will mostly be used to create the basic structure of levels, after which you'll go into the in-game editor to make adjustments. But you certainly can develop entire dungeons using this tool if you find it useful.

## How to use:

You need a dungeon file and one or more level files. (These can all be text files)

The dungeon file is in this format, where each `%(...)` represents a placeholder that you need to fill in:

    [settings]
        save_location = % (where on your computer the XML dungeon should be saved)
        name = % (the dungeon's name
        player_glyph = % (which glyph represents the player)
        floor_glyph = % (which glyph will be used to place a floor tile under any items/enemies/etc that don't have a floor tile specified)
        character = % (which necrodancer character this dungeon is built for
        levels = % (a list of levels in this dungeon)

    [tiles]
        % (a list of definitions of tile glyphs)

    [enemies]
        % (a list of definitions of enemy glyphs)

    [items]
        % (a list of definitions of item glyphs)

    [chests]
        % (a list of definitions of chest glyphs)

    [crates]
        % (a list of definitions of crate/barrel/urn glyphs)

    [shrines]
        % (a list of definitions of shrine glyphs)

    [database]
        % (a lookup table of XML snippets; the other glyph definitions should all reference this section)

Each of the level files is a text file containing glyphs, laid out graphically. 

Look at the files in the `./example` directory; hopefully seeing an example dungeon should make the dungeon format more clear.
    
Run the example from the commandline as follows:

    $ cd example
    $ python3 ../necro_level_editor_helper.py dungeon.txt

In general, you must be in the folder that has your dungeon and level files in it when you run the translator.

## faq:

### How do I define tiles/enemies/items/etc?

Add a new line under the `[database]` heading in your dungeon file. This line will look something like this:

    green_skeleton = <enemy beatDelay="1" lord="0" type="4" x="{x}" y="{y}"></enemy>

Basically, you say `name = xml`, where `name` is a user-friendly name and `xml` is the XML that corresponds to it. **Make sure you include the closing XML tag!!** (in this case, `</enemy>`) The xml should also have two position placeholders: `x="{x}" y="{y}"`.

To define a glyph that corresponds to a green skeleton, add a new line under the `[enemies]` section, like this:

    g = ${database:green_skeleton}

Then, in your actual level file, type a `g` wherever you want to place a green skeleton

### How do I find the XML that corresponds to the various enemies/items/etc in the game?

You have to make a level using the in-game editor, place the type of object you want, save the level, and then examine the game's saved data, which should be located at `C:\Program Files (x86)\Steam\steamapps\common\Crypt of the NecroDancer\dungeons\MY DUNGEON.xml` (for windows users)

Sorry; I know it's a little awkward. As you build many dungeons over time, you should keep your old `[database]` settings, gradually adding new objects to your database as you need them. The example dungeon in `./example/dungeon.txt` already comes with a basic database; I may expand this over time if I get around to it. (Pull requests are welcome!)

### Can I place multiple things in a single space?

Yes! You can place multiple things *of different types* in one space. For example, you can place an enemy, an item, and a floor tile all in a single space, but you can't place multiple enemies or multiple items on a single space. You do this by defining a glyph in multiple different sections. For example, assuming you have the XML for `green_skeleton`, `ice`, and `winged_boots` in your `[database]` section, you can create a glyph `x` that will be converted into a green skeleton that is standing on ice and winged boots with the following:

    [tiles]
        x = ${database:ice}
    [enemies]
        x = ${database:green_skeleton}
    [items]
        x = ${database:winged_boots}

### I used this tool and generated an XML dungeon. When I tried to load it in-game, my game crashed. Help!

That's not technically a question, but I'll humor you. One easy mistake to make is to forget to close the XML tags that you've defined in your `[database]` section. I'm working on a feature that will warn you about this.

If that doesn't fix it, then I'm sorry. Please let me know so that I can fix any bugs that might be in my translator! You can create an issue here on github or you can email me at pancelor@gmail.com.

### Why is this so complicated? Why do I have to mess around with XML? Couldn't you have just have hard-coded certain glyphs to mean certain things?

There are a couple of reasons:

* I wanted to make sure that this tool was extensible and flexible. If I had hard-coded in glyphs for every type of object, then it would be a pain to have to change it every time the game comes out with new objects. Plus, there are hundreds if not thousands of objects in Crypt of the NecroDancer; for example, most enemies can have a `beatDelay` tag in their XML and a `lord` tag, roughly quadrupling the number of glyphs that would need to be hard-coded. I'd much rather let you define objects as needed and bind them to memorable glyphs.

* This format was one of the simplest ways I could think of to get the most immediate benefit. There are certainly more user-friendly programs that I could have made, but this one was one of the simplest ones to program, which means it's less likely to have bugs.

Even though this format might look a little overwhelming at first, it's not bad once you get used to it. The `[database]` section is designed to let you define XML snippets, so that you can define glyphs in the other sections with sane, readable names. Every time you create a new dungeon with this tool, you can copy over your old `[database]` section, so you won't have to muck around with XML too much. 

### Happy level editing!

####-pancelor
