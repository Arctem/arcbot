from tavern.shared import TavernException


class ConflictingTypeAndTrait(TavernException):

    def __init__(self, conflict, *args, **kwargs):
        TavernException.__init__(self, "Both types and traits contained {}.".format(conflict))
