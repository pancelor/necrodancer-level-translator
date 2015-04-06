#!/usr/bin/env python

from string import Template
from sys import argv, exit
from pprint import pprint
import re
from collections import namedtuple


def post(postprocessor):
    def _decorator(fxn):
        def _fxn(*args, **kwargs):
            return postprocessor(fxn(*args, **kwargs))
        return _fxn
    return _decorator

class Instream(object):
    """An object that makes input easier"""
    def __init__(self, fname):
        super(Instream, self).__init__()
        self.generator = self.create_generator(fname)
        self.generator.next()

    def read_lines(self, n):
        return self.generator.send(n)

    def create_generator(self, fname):
        with open(fname, 'r') as file_:
            lines = [(line.strip().split('#')[0]).strip() for line in file_.readlines()]
        num = yield
        while lines:
            out, lines = lines[:num], lines[num:]
            # pprint("out")
            # pprint(out)
            # pprint("lines")
            # pprint(lines)
            num = yield out

class Level(object):
    """Represents a single level in a dungeon"""
    def __init__(self, lines):
        super(Level, self).__init__()
        self.lines = lines
        self.center = (0, 0)
        self.center = self.find_player()

    def find_glyph_coordinates(self, glyph):
        """Returns a list of coordinates of all glyphs in lines that match the given glyph"""
        assert len(glyph) == 1
        for y, _line in enumerate(self.lines):
            for x, char in enumerate(_line):
                if char == glyph:
                    yield x - self.center[0], y - self.center[1]

    def find_player(self, PLAYER_GLYPH='p'): # TODO args
        center = list(self.find_glyph_coordinates(PLAYER_GLYPH))
        if len(center) != 1:
            raise RuntimeError("There are too many (%d) player glyphs ('%s')"%(len(center), PLAYER_GLYPH))
        return center[0]

    # TODO move to dungeon
    # def save(self):
    #     with open("%s.xml"%self.name, 'w') as file_:
    #         file_.writelines(lines)

    def gen_all_chars(self):
        for y, _line in enumerate(self.lines):
            for x, char in enumerate(_line):
                yield (x, y), char

    def __str__(self):
        return '\n'.join(self.lines)

    def __repr__(self):
        return "Level [\n\t%s\n]"%str(self).replace('\n', '\n\t')

def create_translator(glyphs, template_string):
    template = Template(template_string)
    @post(''.join)
    def translator(lines, center):
        for x, y in find_glyph_coordinates(lines, center, glyphs):
            yield template.substitute(x=x, y=y)
    return translator

class Dungeon(object):

    XML_TYPES = [
        "tiles",
        "enemies",
        "items",
        "chests",
        "crates",
        "shrines"
    ]

    def __init__(self, fname):
        super(Dungeon, self).__init__()
        self.name, self.character, self.rosetta, self.level = self.parse_input(fname)
        self.level = Level(self.level.split('\n'))
        pprint(self.name)
        pprint(self.character)
        pprint(self.rosetta)
        pprint(self.level)

    def parse_input(self, fname):
        with open(fname, 'r') as file_:
            file_text = ''.join(file_.readlines())
        flags = re.I | re.M | re.S

        def extract_section(section_name):
            sec = re.search(r'#%s\n+(?P<section>[^#]*?)\n+#'%(section_name), file_text, flags)
            return sec.group("section") if sec else None

        settings = extract_section("settings")
        match = re.match(r"^name\s*=\s*(?P<name>[^\n]+)\ncharacter\s*=\s*(?P<character>[^\n]+)$", settings, flags)
        name = match.group("name")
        character = match.group("character")

        level = extract_section("level") # todo make multiple levels possible

        rosetta = {}
        for xtype in Dungeon.XML_TYPES:
            sec = extract_section(xtype)
            if sec is None:
                raise RuntimeError("Level file is missing section '%s'."%xtype)
            else:
                rosetta[xtype] = sec
        return name, character, rosetta, level

    # def parse_input(self, fname):
    #     XML_TYPES = [
    #         "tiles",
    #         "enemies",
    #         "items",
    #         "chests",
    #         "crates",
    #         "shrines"
    #     ]

    #     def create_pattern(names, sep):
    #         x = r"^" + ''.join(r"%s%s\s*(?P<%s>.*?)\s*"%(name, sep, name) for name in names) + r"$"
    #         print x
    #         print
    #         return x

    #     with open(fname, 'r') as file_:
    #         flags = re.I | re.M | re.S
    #         sections = re.match(
    #             create_pattern(["settings"] + XML_TYPES + ["level", "j"], ":"),
    #             ''.join(file_.readlines()),
    #             flags
    #         ).groupdict()
    #     sections = {k: v.strip() for k, v in sections.items()}

    #     settings = re.match(
    #         create_pattern(["name", "character"], "="),
    #         sections["settings"],
    #         flags
    #     ).groupdict()

    #     pprint (sections["level"])
    #     return_dict = {"settings": settings, "level": sections["level"]}
    #     for xml_tag in XML_TYPES:
    #         if sections[xml_tag]:
    #             return_dict[xml_tag] = {key: val for key, val in [line.split('=') for line in sections[xml_tag].split('\n')]}
    #         else:
    #             return_dict[xml_tag] = {}
    #     return return_dict
    #     # match=re.match(r"name")
    #     # return sections

    def generate_xml(self):
        all_chars = self.level.gen_all_chars()
        for xtype in Dungeon.XML_TYPES:
            for (x, y), char in all_chars:
                if char in self.rosetta[xtype]:
                    pass


def main():
    in_fname = argv[1]


    Dungeon(in_fname)
    # instream = Instream(in_fname)
    # pprint (instream.read_lines(4))
    exit()
    center = find_player(lines)

    translate_floors = create_translator('-mbscvpI*', r"""<tile cracked="0" torch="0" type="0" x="$x" y="$y" zone="0"></tile>""")
    translate_walls = create_translator('x', r"""<tile cracked="0" torch="0" type="100" x="$x" y="$y" zone="0"></tile>""")
    translate_torch_walls = create_translator('t', r"""<tile cracked="0" torch="1" type="100" x="$x" y="$y" zone="0"></tile>""")
    translate_invisible_walls = create_translator('*', r"""<chest color="3" contents="ring_charisma" hidden="0" saleCost="0" singleChoice="0" x="$x" y="$y"></chest>""")
    translate_shovemonsters = create_translator('s', r"""<enemy lord="0" type="212" x="$x" y="$y"></enemy>""")
    translate_red_bats = create_translator('b', r"""<enemy lord="0" type="7" x="$x" y="$y"></enemy>""")
    translate_obsidian_crossbows = create_translator('c', r"""<item bloodCost="0.0" saleCost="0" singleChoice="0" type="weapon_obsidian_crossbow" x="$x" y="$y"></item>""")
    translate_spike_traps = create_translator('v', r"""<trap subtype="-1" type="2" x="$x" y="$y"></trap>""")

    results = [
            "<tiles>",
            translate_floors(lines, center),
            translate_walls(lines, center),
            translate_torch_walls(lines, center),
            "</tiles><traps>",
            translate_spike_traps(lines, center),
            "</traps><enemies>",
            translate_shovemonsters(lines, center),
            translate_red_bats(lines, center),
            "</enemies><items>",
            translate_obsidian_crossbows(lines, center),
            "</items><chests>",
            translate_invisible_walls(lines, center),
            "</chests><shrines></shrines>"
    ]

    set_output(out_fname, results)

if __name__ == '__main__':
    main()

# tiles, traps, enemies, items, chests, crates, shrines