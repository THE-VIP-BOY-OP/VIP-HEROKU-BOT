MODULE_HELP = {}


class ModuleHelp:
    def __init__(self, plugin_name: str, info: str = None):
        self.plugin_name = plugin_name

        # Initialize the plugin with an empty list if not already present
        if plugin_name not in MODULE_HELP:
            MODULE_HELP[plugin_name] = []

        # Add optional info if provided
        if info:
            MODULE_HELP[plugin_name].append({"info": info})

    def add(self, *commands_help):
        """
        Add commands and their help descriptions to the current plugin.
        Supports a list of commands or a single command as a string.
        """
        for command_help in commands_help:
            # Check if the first element is a list (multiple commands)
            if isinstance(command_help[0], list):
                commands = ", ".join(command_help[0])
            else:
                # Single command as a string
                commands = command_help[0]

            help_text = command_help[1]
            MODULE_HELP[self.plugin_name].append([commands, help_text])
        return self
