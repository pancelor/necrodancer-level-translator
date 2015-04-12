#!/usr/bin/env python

from sys import argv
from pprint import pprint
import re
from ConfigParser import RawConfigParser


def post(postprocessor):
    """ Modifies a function so that it's output is first passed through a postprocessor
        e.g. this code snippet:
            @post(list)
            def gen_nums():
                for i in range(1, 4):
                    yield i
            gen_nums()
        gives this output:
            [1, 2, 3]
        (instead of some generator expression)
        """
    def _decorator(fxn):
        def _fxn(*args, **kwargs):
            return postprocessor(fxn(*args, **kwargs))
        return _fxn
    return _decorator

def gen_file_lines(fname):
    """ Reads in a file and returns it as a list of lines, with whitespace stripped off the ends of each line"""
    with open(fname, 'r') as file_:
         return [line.strip() for line in file_.readlines()]

class Level(object):
    """Represents a single level in a dungeon"""
    def __init__(self, fname, player_glyph, floor_glyph):
        super(Level, self).__init__()
        self.lines = gen_file_lines(fname)
        self.center = self._find_player(player_glyph)

        # replace the player with a floor glyph
        y = self.center[1]
        self.lines[y] = self.lines[y].replace(player_glyph, floor_glyph)

    def gen_all_chars(self):
        for y, _line in enumerate(self.lines):
            for x, char in enumerate(_line):
                yield (x - self.center[0], y - self.center[1]), char

    @post(list)
    def _find_glyph_coordinates(self, glyph):
        """Returns a list of coordinates of all glyphs in lines that match the given glyph"""
        assert len(glyph) == 1
        for y, _line in enumerate(self.lines):
            for x, char in enumerate(_line):
                if char == glyph:
                    yield x - self.center[0], y - self.center[1]

    def _find_player(self, player_glyph):
        self.center = (0, 0)
        player_locs = self._find_glyph_coordinates(player_glyph)
        if len(player_locs) != 1:
            raise RuntimeError("There are too many (%d) player glyphs ('%s')"%(len(player_locs), player_glyph))
        return player_locs[0]

    def __str__(self):
        return '\n'.join(self.lines)

    def __repr__(self):
        return "Level [\n\t%s\n]"%str(self).replace('\n', '\n\t')

class Dungeon(object):

    XML_TYPES = [
        "tiles",
        "enemies",
        "items",
        "chests",
        "crates",
        "shrines",
    ]

    def __init__(self, fname):
        super(Dungeon, self).__init__()
        settings, self.rosetta = self._parse_input(fname)

        self.name = settings['name']
        self.character = settings['character']
        self.player_glyph = settings['player_glyph']
        self.floor_glyph = settings['floor_glyph']
        self.level_fnames = settings['levels'].split()
        self.save_location = settings['save_location']

    def save(self):
        with open("%s%s.xml"%(self.save_location, self.name.upper()), 'w') as file_:
            file_.writelines(self._gen_dungeon_xml())

    def _parse_input(self, fname):
        parser = RawConfigParser()
        parser.read(fname)
        config = {
            section: {key: val for key, val in parser.items(section)}
            for section in parser.sections()
        }

        # make sure the sections are exactly what we're expecting
        expected_sections = set(['settings']+Dungeon.XML_TYPES)
        sections = set(config.keys())
        if sections != expected_sections:
            raise RuntimeError("Config file is missing %s and should not include %s."%(str(expected_sections - sections), str(sections - expected_sections)))

        settings = config['settings']
        del config['settings']

        return settings, config

    @post(''.join)
    def _gen_dungeon_xml(self):
        yield r'<?xml?><dungeon character="%s" name="%s" numLevels="%d">'%(self.character, self.name, len(self.level_fnames))
        for level_num, level_fname in enumerate(self.level_fnames):
            yield '<level bossNum="-1" music="0" num="%d">'%(level_num+1)
            yield self._gen_level_xml(level_fname)
            yield '</level>'
        yield '</dungeon>'

    def _ensure_all_characters_are_recognized(self, chars, level_fname):
        for char in chars:
            found = False
            for xtype in Dungeon.XML_TYPES:
                if char in self.rosetta[xtype]:
                    found = True
            if not found:
                raise RuntimeError("Unrecognized character '%s' in level '%s'."%(char, level_fname))

    @post(''.join)
    def _gen_level_xml(self, level_fname):
        level = Level(level_fname, self.player_glyph, self.floor_glyph)
        all_chars = level.gen_all_chars()
        self._ensure_all_characters_are_recognized(
            set(char for (x, y), char in all_chars),
            level_fname
        )

        for xtype in Dungeon.XML_TYPES:
            yield '<%s>'%xtype
            for (x, y), char in all_chars:
                if char in self.rosetta[xtype]:
                    yield self.rosetta[xtype][char]%(x, y)
                elif xtype == 'tiles':
                    yield self.rosetta[xtype][self.floor_glyph]%(x, y)

            yield '</%s>'%xtype


if __name__ == '__main__':
    in_fname = argv[1]

    dungeon = Dungeon(in_fname)
    dungeon.save()
