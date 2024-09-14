# This Bothelp function taken from < https://github.com/The-HellBot/Plugins >
# Credit goes to The-HellBot.
#

BOT_CMD_INFO = {}
BOT_CMD_MENU = {}
BOT_HELP = {}

SYMBOLS = {
    "arrow_left": "«",
    "arrow_right": "»",
    "back": "🔙 back",
    "check_mark": "✔",
    "close": "🗑️",
    "cross_mark": "✘",
    "next": "⤚ next",
    "previous": "prev ⤙",
    "radio_select": "◉",
    "radio_unselect": "〇",
}


class BotHelp:
    _help_instances = {}

    def __new__(cls, category):
        if category in cls._help_instances:
            return cls._help_instances[category]
        instance = super(BotHelp, cls).__new__(cls)
        cls._help_instances[category] = instance
        return instance

    def __init__(self, category: str) -> None:
        if not hasattr(self, "initialized"):
            self.category = category
            self.command_dict = {}
            self.command_info = ""
            self.initialized = True

    def add(self, command: str, description: str):
        self.command_dict[command] = {"command": command, "description": description}
        return self

    def info(self, command_info: str):
        self.command_info = command_info
        return self

    def get_menu(self) -> str:
        result = f"**Plugin Category:** `{self.category}`"
        if self.command_info:
            result += f"\n**Info:** __{self.command_info}__"
        result += "\n\n"
        for command in self.command_dict:
            command_data = self.command_dict[command]
            result += (
                f"**{SYMBOLS['radio_select']} Command:** /{command_data['command']}\n"
            )
            if command_data["description"]:
                result += f"**{SYMBOLS['arrow_right']} Description:** __{command_data['description']}__\n"
            result += "\n"
            BOT_CMD_INFO[command_data["command"]] = {
                "command": command_data["command"],
                "description": command_data["description"],
                "category": self.category,
            }

        return result

    def done(self) -> None:
        BOT_HELP[self.category] = {
            "commands": self.command_dict,
            "info": self.command_info,
        }
        BOT_CMD_MENU[self.category] = self.get_menu()
