from game.gamesrc.latitude.scripts.script import Script
import time
import math

class GameTime(Script):
    def at_script_creation(self):
        self.key = "game_time"
        self.desc = "Keeps track of the game time"
        self.interval = 0
        self.persistent = True
        # Set up the time specification
        self.db.game_epoch = 0 # At this time, the game time was 0:00:00 on the first day of year 0.  Expressed as a unix epoch time.
        self.db.secondsperminute = 60
        self.db.minutesperhour = 60
        self.db.hoursperday = 20
        self.db.daysperyear = 180
        # Configure how the seasons affect the days, etc, and other fancy stuff.
        self.db.dusk_dawn_length = 1800.0 # The length of the dawn after sunrise, in seconds
        self.db.sunrise_sunset_variance = 2.0 # The approximate difference, in hours, between sunrise/sunset at the solstice, and at the equinox.
        self.db.default_lunar_period = 38.0 # The time it takes the moon to orbit the world.  Combined with the length of the year, this is used to determine the phases of the moon.

    def time(self):
        """
        Analagous to time.time(), this returns the seconds since the game epoch.
        """
        return time.time() - self.db.game_epoch

    def localtime(self, at=None):
        """
        Analagous to time.localtime(), this returns a time.struct_time class, so it should be compatible with functions that expect the output from 'localtime'.
        Months and days of the week are not supported, so the date (by month, day-of-month) will always be January 1st.
        """
        if at:
            timeval = int(at)
        else:
            timeval = int(self.time())
        # Seconds
        tm_sec = timeval % int(self.db.secondsperminute)
        timeval /= int(self.db.secondsperminute)
        # Minutes
        tm_min = timeval % int(self.db.minutesperhour)
        timeval /= int(self.db.minutesperhour)
        # Hours
        tm_hour = timeval % int(self.db.hoursperday)
        timeval /= int(self.db.hoursperday)
        # Days
        tm_wday = timeval % 7
        tm_yday = timeval % int(self.db.daysperyear)
        timeval /= int(self.db.daysperyear)
        tm_yday += 1 # Starts at 1, not 0
        # Years
        tm_year = timeval
        # Return the result
        return(time.struct_time((tm_year, 1, 1, abs(tm_hour), abs(tm_min), abs(tm_sec), abs(tm_wday), abs(tm_yday), 0)))

    def mktime(self, t):
        """
        Analagous to time.mktime(), this is te inverse function of self.localtime().
        It takes a struct_time as constructed by this class, and converts it back to a 'game epoch' time value.
        """
        # Years
        timeval = t.tm_year
        timeval *= int(self.db.daysperyear)
        # Days
        timeval += t.tm_yday - 1 # Counts from 1, not 0
        timeval *= int(self.db.hoursperday)
        # Hours
        timeval += t.tm_hour
        timeval *= int(self.db.minutesperhour)
        # Minutes
        timeval += t.tm_min
        timeval *= int(self.db.secondsperminute)
        # Seconds
        timeval += t.tm_sec
        return timeval

    def today_sunrise(self, at=None):
        localtime = self.localtime(at)
        # Calculate the time of sunrize on the equinox
        sunrise_hour = float(self.db.hoursperday) * 0.25
        # Get the fractional year in radians, and take the cosine to calculate the amount to vary the sunrise time.
        variance_factor = math.cos(float(localtime.tm_yday) / float(self.db.daysperyear) * 2.0 * math.pi)
        # Get the sunrise hour today
        sunrise_hour += variance_factor * float(self.db.sunrise_sunset_variance)
        sunrise_minute = math.modf(sunrise_hour)[0] * float(self.db.minutesperhour)
        sunrise_second = math.modf(sunrise_minute)[0] * float(self.db.secondsperminute)
        # Calculate the 'game epoch' value and return it.
        return(self.mktime(time.struct_time((localtime.tm_year, 1, 1, int(sunrise_hour), int(sunrise_minute), int(sunrise_second), localtime.tm_wday, localtime.tm_yday, 0))))

    def today_sunset(self, at=None):
        localtime = self.localtime(at)
        # Calculate the time of sunrize on the equinox
        sunset_hour = float(self.db.hoursperday) * 0.75
        # Get the fractional year in radians, and take the negative cosine to calculate the amount to vary the sunset time.
        variance_factor = - math.cos(float(localtime.tm_yday) / float(self.db.daysperyear) * 2.0 * math.pi)
        # Get the sunset hour today
        sunset_hour += variance_factor * float(self.db.sunrise_sunset_variance)
        sunset_minute = math.modf(sunset_hour)[0] * float(self.db.minutesperhour)
        sunset_second = math.modf(sunset_minute)[0] * float(self.db.secondsperminute)
        # Calculate the 'game epoch' value and return it.
        return(self.mktime(time.struct_time((localtime.tm_year, 1, 1, int(sunset_hour), int(sunset_minute), int(sunset_second), localtime.tm_wday, localtime.tm_yday, 0))))

    def today(self, at=None):
        """
        Returns the time of midnight this morning in game epoch format
        """
        if at:
            at = int(at)
        else:
            at = self.time()
        seconds_per_day = int(self.db.secondsperminute) * int(self.db.minutesperhour) * int(self.db.hoursperday)
        return at - at % seconds_per_day

    def type_daytime(self, at=None):
        """
        Returns 'night', 'dawn', 'day', or 'dusk'.
        """
        if at:
            at = int(at)
        else:
            at = self.time()
        today_sunrise = self.today_sunrise(at)
        today_sunset = self.today_sunset(at)
        if abs(at - today_sunrise) < float(self.db.dusk_dawn_length):
            return 'dawn'
        if abs(at - today_sunset) < float(self.db.dusk_dawn_length):
            return 'dusk'
        if at >= today_sunrise and at <= today_sunset:
            return 'day'
        return 'night'

    def type_season(self, at=None):
        """
        Returns 'winter', 'spring', 'summer', or 'fall'.
        """
        localtime = self.localtime(at)
        season = int(float(localtime.tm_yday) / float(self.db.daysperyear) * 4.0)
        return {0 : 'winter', 1 : 'spring', 2 : 'summer', 3 : 'fall'}[season]

    def lunar_phase(self, at=None, lunar_period=None):
        """
        Returns the position in the lunar cycle.  0.0 = New Moon, 0.25 = First Quarter, 0.5 = Full Moon, 0.75 = Third Quarter, etc.
        """
        if lunar_period:
            lunar_period = float(lunar_period)
        else:
            lunar_period = float(self.db.default_lunar_period)
        localtime = self.localtime(at)
        # Add together the position in the period of the world's orbit, with the position in the period of the moon's orbit to get the moon phase position
        world_position = float(localtime.tm_yday) / float(self.db.daysperyear)
        lunar_position = (float(localtime.tm_year) * float(self.db.daysperyear) + float(localtime.tm_yday)) % lunar_period / lunar_period
        return((world_position + lunar_position) % 1.0)

    def type_moon(self, at=None, lunar_period=None):
        """
        Returns 'new_moon', 'waxing_crescent', 'first_quarter', 'waxing_gibbous', 'full_moon', 'waning_gibbous', 'third_quarter' or 'waning_crescent'.
        """
        seconds_per_day = int(self.db.secondsperminute) * int(self.db.minutesperhour) * int(self.db.hoursperday)
        # Calculate the nearest midnight.
        if at:
            at = int(at)
        else:
            at = self.time()
        at += seconds_per_day / 2
        at -= at % seconds_per_day
        # Get the lunar phases from yesterday, today, and tomorrow
        lunar_phase_yesterday = self.lunar_phase(at=at - seconds_per_day, lunar_period=lunar_period)
        lunar_phase_today = self.lunar_phase(at=at, lunar_period=lunar_period)
        lunar_phase_tomorrow = self.lunar_phase(at=at + seconds_per_day, lunar_period=lunar_period)
        # Is today the closest day to the first quarter?
        if abs(0.25 - lunar_phase_today) <= abs(0.25 - lunar_phase_tomorrow) and abs(0.25 - lunar_phase_today) < abs(0.25 - lunar_phase_yesterday):
            return 'first_quarter'
        # Is today the closest day to the full moon?
        if abs(0.5 - lunar_phase_today) <= abs(0.5 - lunar_phase_tomorrow) and abs(0.5 - lunar_phase_today) < abs(0.5 - lunar_phase_yesterday):
            return 'full_moon'
        # Is today the closest day to the third quarter?
        if abs(0.75 - lunar_phase_today) <= abs(0.75 - lunar_phase_tomorrow) and abs(0.75 - lunar_phase_today) < abs(0.75 - lunar_phase_yesterday):
            return 'third_quarter'
        # Is today the closest day to the new moon?
        if abs(0.5 - lunar_phase_today) >= abs(0.5 - lunar_phase_tomorrow) and abs(0.5 - lunar_phase_today) > abs(0.5 - lunar_phase_yesterday):
            return 'new_moon'
        # Today isn't special.  Return the lunar phase
        return({0 : 'waxing_crescent', 1 : 'waxing_gibbous', 2 : 'waning_gibbous', 3: 'waning_crescent'}[int(lunar_phase_today * 4.0)])
