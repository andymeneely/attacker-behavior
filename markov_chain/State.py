#!/usr/bin/env python3

class State():
    """ A `State` object represents a given state in a markov chain. """

    def __init__(self, label, info={}):
        """
        Constructor. Create `State` object.

        Arguments:
        label   label or name of the `State`
        info    other information about the `State`, as necessary
        """
        assert type(info) == dict
        self._label = label
        self._info = info

    def getLabel(self):
        """ Return `self._label`. """
        return self._label

    def getInfo(self):
        """ Return `self._info`. """
        return self._info

    def setInfo(self, new_info):
        """ Set `self._info` to `new_info`. """
        assert type(new_info) == dict
        self._info = new_info

    def __dict__(self):
        """ Return custom dictionary representation of the `State` object. """
        return {
            "label": self._label,
            "info": self._info
        }

    def __str__(self):
        """ Return custom string representation of the `State` object. """
        return str(self.__dict__())


