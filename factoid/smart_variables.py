import random
import re

from ircbot.plugin import IRCPlugin
from ircbot.events import sendmessage, sendaction
import ircbot.user_controller as user_controller

import arcuser.arcuser_controller as arcuser_controller

variables_regex = re.compile(r'(\$[a-zA-Z]+)')
directed_regex = re.compile(r'^\S+(?=[:,])')


class SmartVariables(IRCPlugin):
    '''We call each callback with the metadata and a list of the variables found.
    They return a dict containing the variables they reply with.'''

    def __init__(self):
        super(SmartVariables, self).__init__()
        self.callbacks = set()

    def sendsmartmessage(self, target, message, **kwargs):
        message = self.perform_replacements(message, **kwargs)
        self.fire(sendmessage(target, message))

    def sendsmartaction(self, target, action, **kwargs):
        action = self.perform_replacements(action, **kwargs)
        self.fire(sendaction(target, action))

    def perform_replacements(self, message, **kwargs):
        replaced = {}
        kwargs = self.process_kwargs(**kwargs)
        replacements = self.gather_replacements(**kwargs)

        parts = variables_regex.split(message)
        print(parts)
        for i in range(len(parts)):
            part = parts[i]
            if not part or part[0] != '$':
                continue
            part = part[1:]
            if part in replacements.keys():
                replacement_func = random.choice(replacements[part])
                parts[i] = str(replacement_func())
        print(parts)
        return ''.join(parts)

    def gather_replacements(self, **metadata):
        replacements = {}
        for callback in self.callbacks:
            retval = callback(**metadata)
            for key, value in retval.items():
                if key not in replacements:
                    replacements[key] = []
                replacements[key].append(value)
        return replacements

    def process_kwargs(self, **kwargs):
        if 'original' in kwargs:
            message = kwargs['original']
            message_parse = directed_regex.findall(message)
            if message_parse:
                target = message_parse[0]
                user = user_controller.get_or_create_user(target)
                arcuser = arcuser_controller.get_or_create_arcuser(user)
                kwargs['target'] = arcuser
        return kwargs

    def registersmartvariable(self, callback):
        self.callbacks.add(callback)
