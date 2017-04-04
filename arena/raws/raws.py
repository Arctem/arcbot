from arena.raws.raws_data import data, Type

races = list(filter(lambda r: data[r]['type'] is Type.RACE, data))
weapons = list(filter(lambda r: data[r]['type'] is Type.WEAPON, data))
