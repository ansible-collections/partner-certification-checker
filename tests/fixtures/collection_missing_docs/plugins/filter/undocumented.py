from __future__ import absolute_import, division, print_function

__metaclass__ = type


class FilterModule:
    def filters(self):
        return {
            "undocumented": self.undocumented,
        }

    @staticmethod
    def undocumented(value):
        return value
