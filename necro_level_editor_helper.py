from string import Template
from sys import argv


def post(postprocessor):
    def _decorator(fxn):
        def _fxn(*args, **kwargs):
            return postprocessor(fxn(*args, **kwargs))
        return _fxn
    return _decorator

def get_input(fname):
    with open(fname, 'r') as file_:
        return file_.readlines()

def set_output(fname, lines):
    if type(lines) != type([]):
        lines = [lines]
    with open(fname, 'w') as file_:
        file_.writelines(lines)

def find_glyph_coordinates(lines, center, glyphs):
    """ Returns a list of coordinates of all glyphs in lines that match any character in the given glyph string """
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in glyphs:
                yield x - center[0], y - center[1]

def find_player(lines, PLAYER_GLYPH='p'):
    center = list(find_glyph_coordinates(lines, (0, 0), PLAYER_GLYPH))
    if len(center) != 1:
        raise RuntimeError("Make sure there's only one player (%s)"%PLAYER_GLYPH)
    return center[0]

def create_translator(glyphs, template_string):
    template = Template(template_string)
    @post(''.join)
    def translator(lines, center):
        for x, y in find_glyph_coordinates(lines, center, glyphs):
            yield template.substitute(x=x, y=y)
    return translator

def main():
    in_fname, out_fname = argv[1], argv[2]

    lines = get_input(in_fname)
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