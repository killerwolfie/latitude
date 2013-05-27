from ev import default_cmds, search_script

class CmdSysGameTime(default_cmds.MuxPlayerCommand):
    """
    @gametime - Display the current game world time.
    """

    key = "@gametime"
    aliases = ['mucktime', '@time']
    locks = "cmd:all()"
    help_category = "General"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    moon_names = {
        'new' : '{xNew{n',
        'waxing_crescent' : '{Wwaxing qrescent{n',
        'first_quarter' : '{Wfirst quarter{n',
        'waxing_gibbous' : '{Wwaxing gibbous{n',
        'full' : '{wFull{n',
        'waning_gibbous' : '{Wwaning gibbous{n',
        'third_quarter' : '{Wlast quarter{n',
        'waning_crescent' : '{Wwaning crescent{n',
    }

    season_names = {
        'winter' : '{wwinter{n',
        'spring' : '{Gspring{n',
        'summer' : '{gsummer{n',
        'fall' : '{Yautumn{n',
    }

    daytime_names = {
        'dawn' : '{Ydawn{n',
        'day' : '{yday{n',
        'dusk' : '{Ydusk{n',
        'night' : '{Bnight{n',
    }

    def func(self):
        game_time = search_script('game_time')
        if not game_time:
            self.msg('{RThe game time system is not configured on this server.')
            return
        game_time = game_time[0]
        # Get the current time details
        game_time_now = game_time.localtime()
        type_daytime = game_time.type_daytime()
        type_season = game_time.type_season()
        type_moon = game_time.type_moon()
        # Output the time information
        self.msg('{n/================---------------------')
        self.msg('{n| It is %s, in %s.' % (self.daytime_names[type_daytime], self.season_names[type_season]))
        if type_daytime != 'day':
            self.msg('{n| It\'s a %s moon tonight.' % (self.moon_names[type_moon]))
        self.msg('{n|')
        self.msg('{n| {bCurrent date:{n Day %d, of year %d' % (game_time_now.tm_yday, game_time_now.tm_year))
        self.msg('{n| {bCurrent time:{n %02d:%02d:%02d' % (game_time_now.tm_hour, game_time_now.tm_min, game_time_now.tm_sec))
        self.msg('{n|')
        self.msg('{n| {bGame Time:{n')
        self.msg('{n|   %d seconds per minute.' % (game_time.db.secondsperminute))
        self.msg('{n|   %d minutes per hour.' % (game_time.db.minutesperhour))
        self.msg('{n|   %d hours per day.' % (game_time.db.hoursperday))
        self.msg('{n|   %d days per year.' % (game_time.db.daysperyear))
        self.msg('\:::::::::::...........')
 
