from circuits import Event

class sendsmartmessage(Event):
    """Send a PRIVMSG to the server with variable replacements."""

class sendsmartaction(Event):
    """Send a PRIVMSG to the server with ACTION formatting and variable replacements."""

class registersmartvariable(Event):
    """Register a callback for SmartVariables."""
