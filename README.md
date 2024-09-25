# Radhe radhe

### How to add plugins


#### Example Script

```python
from Vivek import app  # This is the Pyrogram client
from pyrogram import filters  # Pyrogram filters
from pyrogram.types import Message
from Vivek.functions.help import ModuleHelp  # For module help

# 'filters.sudo' is used for commands that can only be executed by the bot owner or self
@app.on_message(filters.sudo & filters.command("example_command"))
async def start_command(client, message: Message):
    await message.reply_text("This is an example module.")

@app.on_message(filters.sudo & filters.command(["example_command1", "example_command2"]))
async def help_command(client, message: Message):
    await message.reply_text("This is an example help module.")

# Initialize ModuleHelp for this plugin
help = ModuleHelp("example_plugin", "This plugin does XYZ.")
#                             |                    |
#                             |                    └─ Optional info about the plugin (string)
#                             └─ Name of the plugin

# Add command help descriptions
help.add(
    (["example_command1", "example_command2"], "Example command help"),  # List of commands with their help description
    ("example_command", "Example help for command")  # Single command with its help description
)
#         |                             |
#         |                             └─ Command description
#         └─ List of command names (can be multiple)

```
And add you plugins in  Folder's [Vivek/plugins](https://github.com/Vivekkumar-in/Vivek/blob/master/Vivek/plugins) In sub folder according to your script type

##### This Project is Licensed under [MIT License](https://github.com/Vivekkumar-IN/Vivek/blob/master/LICENSE)",

