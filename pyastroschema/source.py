"""Eventually this will be generalized from 'source' specifically to any 'struct'.
"""

from collections import OrderedDict

from . import SCHEMA_KEYS


class Keys:

    def __init__(self, schema):
        props = schema[SCHEMA_KEYS.PROPS]
        for prop_name in props.keys():
            setattr(self, prop_name.upper(), prop_name)



    def keys(self):
        def _test_key(key):
            if key.startswith('_'):
                return False
            if callable(getattr(self, key)):
                return False
            return True

        keys = [kk for kk in dir(self) if _test_key(kk)]
        return keys

