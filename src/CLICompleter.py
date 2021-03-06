from .ChatCommands import ChatCommands as CMD
from .DefaultEmojis import emojis as default_emojis
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer, Completion
import re


class CLICompleter(Completer):
    def __init__(self, guild_emojis, guild):
        Completer.__init__(self)
        self.guild_emojis = guild_emojis
        self.default_emojis = list(default_emojis)
        self.guild = guild
        self.channels = guild.text_channels

    def get_completions(self, document, complete_event):
        text = document.text
        cmds = [cmd.split(' ')[0] for cmd in CMD.get_command_list(True)]
        emoji_re = re.findall(r':([\S]*?)$', text)
        channel_re = re.findall(r'#([\S]*?)$', text)
        tag_re = re.findall(r'@([^@]{,32})$', text)

        if text.startswith('/'):
            for c in cmds:
                if text in c:
                    yield Completion(c, -len(text))
        elif emoji_re:
            emoji = emoji_re[0]
            for e in self.default_emojis + self.guild_emojis:
                if emoji.lower() in e.lower():
                    yield Completion(e, -len(emoji) - 1)
        elif channel_re:
            for c in self.channels:
                channel_name = '#' + c.name
                channel = channel_re[0]
                if channel.lower() in channel_name.lower():
                    yield Completion(channel_name, -len(channel) - 1)
        elif tag_re:
            for g in self.guild.members:
                tag = tag_re[-1]
                names = [g.name.lower()]
                if g.nick:
                    names.append(g.nick.lower())
                for name in names:
                    if tag in name:
                        yield Completion(g.display_name, -len(tag))
