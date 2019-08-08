import functools

import attr


asdict = attr.asdict
struct = functools.partial(attr.s, auto_attribs=True)