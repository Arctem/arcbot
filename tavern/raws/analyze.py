import dungeon
import job
import monster


def combine_dicts(base, add):
    for key, val in add.items():
        if key in base:
            base[key] += val
        else:
            base[key] = val
    return base

total_str = dict()
total_weak = dict()
monster_uses = {name: 0 for name in monster.stocks.keys() | monster.modifiers.keys()}

for name, d in dungeon.types.items():
    options = monster.get_monster_options(d.monster_reqs, d.monster_opts)
    strengths = dict()
    weaknesses = dict()
    for opt in options['required'] | options['optional']:
        monster_uses[opt.name] += 1
        for strength in opt.strengths:
            if strength in strengths:
                strengths[strength] += 1
            else:
                strengths[strength] = 1
        for weakness in opt.weaknesses:
            if weakness in weaknesses:
                weaknesses[weakness] += 1
            else:
                weaknesses[weakness] = 1
    print('{}:'.format(name.capitalize()))
    print('Strong against:\n{}'.format(
        '\n'.join(['\t{}: {}'.format(key.capitalize(), val) for key, val in strengths.items()])))
    print('Weak against:\n{}'.format(
        '\n'.join(['\t{}: {}'.format(key.capitalize(), val) for key, val in weaknesses.items()])))

    total_str = combine_dicts(total_str, strengths)
    total_weak = combine_dicts(total_weak, weaknesses)


print('\n\nTotal:')
print('Strong against:\n{}'.format(
    '\n'.join(['\t{}: {}'.format(key.capitalize(), val) for key, val in sorted(total_str.items())])))
print('Weak against:\n{}'.format(
    '\n'.join(['\t{}: {}'.format(key.capitalize(), val) for key, val in sorted(total_weak.items())])))

print('\n\nMonster Uses:')
print('\n'.join(['\t{}: {}'.format(key.capitalize(), val) for key, val in sorted(monster_uses.items())]))
