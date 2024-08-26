class HandlerManager:
    def __init__(self):
        self.handler_list = {}

    def add_to_handler_list(self, commands, handler_func):
        for command in commands:
            self.handler_list[command] = handler_func

    def get_handler(self, command):
        return self.handler_list.get(command)

    def get_all_handlers(self):
        handler_info = []
        for command, func in self.handler_list.items():
            handler_info.append(f"Command: {command} - Function: {func.__name__}")
        return "\n".join(handler_info)