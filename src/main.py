import sims4.commands

# ello world [first script for noobs]

@sims4.commands.Command('hellow', command_type=sims4.commands.CommandType.Live)
def _hellow(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("this is my first script mod")
