import ircbot.storage as db
import tavern.dungeon.controller as dungeon_controller
import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller
import tavern.util.tutorial as tutorial
from tavern.tavern_models import (HeroActivity, Tavern, TavernDungeon,
                                  TavernHero)


class HQ():

    def __init__(self, plugin):
        self.plugin = plugin

    @db.atomic
    def name(self, arcuser, channel, args, s=None):
        if len(args) is 0:
            self.plugin.say(
                channel, '{}: Please name your tavern with ".tavern name <tavern name>"'.format(arcuser.base.nick))
        else:
            tavern = hq_controller.name_tavern(arcuser, args, s=s)
            if tavern:
                self.plugin.say(channel, '{}: Your tavern is now named {}.'.format(arcuser.base.nick, tavern.name))

                tavern = hq_controller.find_tavern(arcuser, s=s)
                resident_hero = tavern.resident_hero
                if not tavern.resident_hero:
                    resident_hero = hq_controller.create_resident_hero(tavern, s=s)

                self.plugin.say(channel, '{}: Your tavern has a resident hero. Their name is {}.'.format(
                    arcuser.base.nick, resident_hero))
            else:
                self.plugin.say(channel, '{}: Unable to name tavern.'.format(arcuser.base.nick))

    @tutorial.tutorial_lock
    @db.needs_session
    def status(self, arcuser, channel, args, s=None):
        messages = []

        tavern = hq_controller.find_tavern(arcuser, s=s)
        if args in ['', 'tavern']:
            if not tavern:
                messages.append('Please name your tavern with ".tavern name <tavern name>" first.')
            else:
                messages.append('You own the tavern {}. You have {} gold.'.format(tavern.name, tavern.money))
                messages.append('Your resident hero is {}.'.format(tavern.resident_hero))
                if tavern.hired_hero:
                    messages.append('You have hired {}.'.format(tavern.hired_hero))
                for visitor in tavern.visiting_heroes:
                    messages.append('{} is visiting your tavern.'.format(visitor.name))
        elif args == 'heroes':
            heroes = pool_controller.get_heroes(s=s)
            heroes = {
                activity: list(map(
                    lambda h: h.name,
                    filter(lambda h: h.activity is activity, heroes)
                )) for activity in HeroActivity
            }
            if len(heroes[HeroActivity.Elsewhere]) > 0:
                messages.append('{} are taking the day off.'.format(', '.join(heroes[HeroActivity.Elsewhere])))

            if len(heroes[HeroActivity.CommonPool]) > 0:
                messages.append('{} are visiting the town square.'.format(
                    ', '.join(heroes[HeroActivity.CommonPool])))
            else:
                messages.append('No one is visiting the town square.')

            if len(heroes[HeroActivity.VisitingTavern]) > 0:
                messages.append('{} are visiting taverns.'.format(', '.join(heroes[HeroActivity.VisitingTavern])))
            if len(heroes[HeroActivity.Hired]) > 0:
                messages.append('{} have been hired.'.format(', '.join(heroes[HeroActivity.Hired])))
            if len(heroes[HeroActivity.Adventuring]) > 0:
                messages.append('{} are out adventuring.'.format(', '.join(heroes[HeroActivity.Adventuring])))

            injured_heroes = list(
                map(lambda h: h.name,
                    filter(lambda h: h.injured, pool_controller.get_heroes(s=s))))
            if len(injured_heroes) > 0:
                messages.append('{} are injured.'.format(', '.join(injured_heroes)))
        elif args == 'dungeons':
            dungeons = dungeon_controller.get_known_dungeons(s=s)
            if len(dungeons) == 0:
                messages.append('No dungeons are known of.')
            for dungeon in dungeons:
                message = '{} has {} floors.'.format(dungeon.name, len(dungeon.floors))
                hero_count = dungeon_controller.get_heroes_in_dungeon(dungeon, s=s)
                if hero_count > 0:
                    message += ' There are {} heroes inside.'.format(hero_count)
                messages.append(message)
        else:
            options = hq_controller.search_taverns(
                args, s=s) + pool_controller.search_heroes(args, s=s) + dungeon_controller.search_dungeons(args, s=s)
            if len(options) == 1:
                messages += make_long_description(options[0])
            elif len(options) == 0:
                messages.append('Could not find {}.'.format(args))
            else:
                messages.append('Found {} results. Please specify: {}'.format(
                    len(options), ', '.join(map(str, options))))

        for message in messages:
            self.plugin.say(channel, '{}: {}'.format(arcuser.base.nick, message))


@db.needs_session
def make_long_description(entity, s=None):
    if isinstance(entity, Tavern):
        return hq_controller.tavern_details(entity, s=s)
    if isinstance(entity, TavernHero):
        return pool_controller.hero_details(entity, s=s)
    if isinstance(entity, TavernDungeon):
        return dungeon_controller.dungeon_details(entity, s=s)
