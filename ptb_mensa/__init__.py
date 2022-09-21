# ptb_mensa - Retrieve the PTB mensa's (in Berlin) menu
# Copyright (C) 2022 Hans Niklas Jacob
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime

from . import intern
from .intern import Menu, DayMenu

__WEEK_NR__   = None
__WEEK_MENUS__ = None
__WEEK_DATES__ = None

def __update__():
  global __WEEK_NR__
  global __WEEK_MENUS__
  global __WEEK_DATES__
  week_nr = datetime.date.today().isocalendar()[1]
  if __WEEK_MENUS__ is None or __WEEK_NR__ != week_nr:
    __WEEK_NR__ = week_nr
    __WEEK_MENUS__,__WEEK_DATES__ = intern.get_week_menus()
    __WEEK_MENUS__ += ["Closed", "Closed"]
    __WEEK_DATES__ += ["Samstag", "Sonntag"]

def week_dates():
  global __WEEK_DATES__
  __update__()
  return __WEEK_DATES__[:5]

def week_menus():
  global __WEEK_MENUS__
  __update__()
  return __WEEK_MENUS__[:5]

def date():
  global __WEEK_DATES__
  __update__()
  weekday = datetime.date.today().weekday()
  return __WEEK_DATES__[weekday]

def menu():
  global __WEEK_MENUS__
  __update__()
  weekday = datetime.date.today().weekday()
  return __WEEK_MENUS__[weekday]

