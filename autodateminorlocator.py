from  matplotlib.dates import AutoDateLocator, rrulewrapper, MicrosecondLocator, RRuleLocator
from datetime import timedelta
import numpy as np

class AutoDateMinorLocator(AutoDateLocator):

    def __init__(self, *args, **kwargs):
        AutoDateLocator.__init__(self, *args, **kwargs)
        freqs = self._freqs
        self._freqconverter = {
                freqs[0]: lambda x: x / 365.,
                freqs[1]: lambda x: x / 31.,
                freqs[2]: lambda x: x,
                freqs[3]: lambda x: x * 24,
                freqs[4]: lambda x: x * 24 * 60,
                freqs[5]: lambda x: x * 24 * 60 * 60,
                freqs[6]: lambda x: x * 24 * 60 * 60 * 1000000
                }

    @staticmethod
    def freq_to_index(freq):
        return {0: 0,
                1: 1,
                3: 2,
                4: 3,
                5: 4,
                6: 5}[freq]

    @staticmethod
    def next_freq(freq):
        return {0: 1,
                1: 3,
                3: 4,
                4: 5,
                5: 6}[freq]

    def get_locator(self, dmin, dmax):
        # get the recommended tick locations from AutoDateLocator, then
        # go one level more numerous ticks
        self.old_refresh()
        major_freq = self._freq
        tick_locations = self._old_locator.tick_values(dmin, dmax)
        tick_dt = tick_locations[1] - tick_locations[0]
        # tick_dt is in terms of days. convert it to major_freq
        dt = self._freqconverter[major_freq](tick_dt)
        # Check each possible interval of self._freq
        minor_interval = 0
        minor_interval_index = 0
        minor_freq = major_freq
        for i, interval in enumerate(self.intervald[major_freq]):
            if dt-.5 > interval:
                minor_interval = interval
                minor_interval_index = i
            else:
                break
        if minor_interval == 0:
            # Then we need to go to the next smaller time interval
            minor_freq = self.next_freq(major_freq)
            minor_interval = self.intervald[minor_freq][-3]
            minor_interval_index = len(self.intervald[minor_freq]) - 3
        byranges = [None, 1, 1, 0, 0, 0, None]
        for i, freq in enumerate(self._freqs):
            if freq != minor_freq:
                byranges[i] = None
            else:
                break
        minor_freq_index = self.freq_to_index(minor_freq)
        byranges[minor_freq_index] = self._byranges[minor_freq_index]
        if minor_freq != self._freqs[-1]:
            _, bymonth, bymonthday, byhour, byminute, bysecond, _ = byranges
            rrule = rrulewrapper(minor_freq, interval=minor_interval,
                    dtstart=dmin, until=dmax, bymonth=bymonth,
                    bymonthday=bymonthday, byhour=byhour,
                    byminute=byminute, bysecond=bysecond)
            locator = RRuleLocator(rrule, self.tz)
        else:
            locator = MicrosecondLocator(minor_interval, tz=self.tz)
        locator.set_axis(self.axis)
        locator.set_view_interval(*self.axis.get_view_interval())
        locator.set_data_interval(*self.axis.get_data_interval())
        return locator


    def old_refresh(self):
        dmin, dmax = self.viewlim_to_dt()
        self._old_locator = AutoDateLocator.get_locator(self, dmin,
                dmax)
