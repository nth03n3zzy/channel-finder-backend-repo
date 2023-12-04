class Game:
    def __init__(self, team, date, opponent, time, channel):
        self.team = team
        self.date = date
        self.opponent = opponent.title()
        self.time = time
        # Check if channel is a list, and if so, capitalize each element.
        if isinstance(channel, list):
            self.channel = [c.upper() for c in channel]
        else:
            self.channel = [channel.upper()]

    def __str__(self):
        channel_str = ', '.join(self.channel)
        return f"Team: {self.team}, Date: {self.date}, Opponent: {self.opponent}, Time: {self.time}, Channel: {channel_str}"
