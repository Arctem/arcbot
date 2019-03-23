import tavern.dungeon.controller as dungeon_controller
import tavern.hq.controller as hq_controller
import tavern.pool.controller as pool_controller
import tavern.util.tutorial as tutorial

from tavern.tavern_models import HeroActivity


class HQ():

    def __init__(self, plugin):
        self.plugin = plugin

    def create(self, arcuser, channel, args):
        if len(args) is 0:
            self.plugin.say(
                channel, '{}: Please name your tavern with ".tavern name <tavern name>"'.format(arcuser.base.nick))
        else:
            tavern = hq_controller.name_tavern(arcuser, args)
            if tavern:
                self.plugin.say(channel, '{}: Your tavern is now named {}.'.format(arcuser.base.nick, tavern.name))

                tavern = hq_controller.find_tavern(arcuser)
                resident_hero = tavern.resident_hero
                if not tavern.resident_hero:
                    resident_hero = hq_controller.create_resident_hero(tavern)

                self.plugin.say(channel, '{}: Your tavern has a resident hero. Their name is {}.'.format(
                    arcuser.base.nick, resident_hero))
            else:
                self.plugin.say(channel, '{}: Unable to name tavern.'.format(arcuser.base.nick))

    @tutorial.tutorial_lock
    def status(self, arcuser, channel, args):
        messages = []

        tavern = hq_controller.find_tavern(arcuser)
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
            heroes = pool_controller.get_heroes()
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
        elif args == 'dungeons':
            dungeons = dungeon_controller.get_known_dungeons()
            if len(dungeons) == 0:
                messages.append('No dungeons are known of.')
            for dungeon in dungeons:
                message = '{} has {} floors.'.format(dungeon.name, len(dungeon.floors))
                hero_count = dungeon_controller.get_heroes_in_dungeon(dungeon.id)
                if hero_count > 0:
                    message += ' There are {} heroes inside.'.format(hero_count)
                messages.append(message)
        else:
            options = hq_controller.search_taverns(
                args) + pool_controller.search_heroes(args) + dungeon_controller.search_dungeons(args)
            if len(options) == 1:
                messages += options[0].details_strings()
            elif len(options) == 0:
                messages.append('Could not find {}.'.format(args))
            else:
                messages.append('Found {} results. Please specify: {}'.format(
                    len(options), ', '.join(map(str, options))))

        for message in messages:
            self.plugin.say(channel, '{}: {}'.format(arcuser.base.nick, message))
