import random
import re

from ircbot.plugin import IRCPlugin
from ircbot.events import sendmessage, sendaction
import ircbot.user_controller as user_controller

import arcuser.arcuser_controller as arcuser_controller

variables_regex = re.compile(r'(?<=\$)[a-zA-Z]+')
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
        found_vars = variables_regex.findall(message)
        kwargs = self.process_kwargs(**kwargs)
        replacements = self.gather_replacements(found_vars, **kwargs)
        #this is so if a variable name is a prefix of another we won't break when replacing them
        replacements = sorted(replacements.items(), key=lambda r: len(r[0]), reverse=True)

        for to_replace, options in replacements:
            replacement = random.choice(options)
            message = re.sub(r'\${}(?![a-zA-Z])'.format(to_replace), replacement, message)
        return message

    def gather_replacements(self, variables, **metadata):
        replacements = {}
        for callback in self.callbacks:
            retval = callback(variables, **metadata)
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
