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

import sys
from prettytable import PrettyTable
import shutil

import ptb_mensa

# printing functions

def get_terminal_width():
  return shutil.get_terminal_size((400, 20))[0]

def add_today_column(table, name, menu):
  table.add_column(name, [menu.description, menu.extra, menu.price[0], menu.price [1]])

def print_today():
  table = PrettyTable(title=f"PTB Mensa Menu {ptb_mensa.date()}")
  menu = ptb_mensa.menu()
  table.add_column("", ["Menu", "Extra", "Preis (intern)", "Preis (extern)"], align="r")
  add_today_column(table, "Vegan", menu.vegan)
  add_today_column(table, "Vegetarisch", menu.veggi)
  add_today_column(table, "Fleisch", menu.meat)
  add_today_column(table, "Suppe", menu.soup)
  table.min_width = 7
  table.max_width = 35
  table.max_table_width = get_terminal_width() - 6
  print(table)



def add_week_column(table, name, menus):

  column = [menus[0].description, menus[0].extra]
  for menu in menus[1:]:
    column += ["-"*30, menu.description, menu.extra]

  column += ["-"*30, menus[0].price[0], menus[0].price[1]]

  table.add_column(name, column)

def print_week():
  table = PrettyTable(title=f"PTB Mensa Menu")
  menu = ptb_mensa.week_menus()
  days = ptb_mensa.week_dates()

  head_col = [days[0], "", ""]
  for day in days[1:]:
    head_col += [day, "", ""]

  head_col += ["Peris (intern)","Preis (extern)"]

  table.add_column("", head_col, align="r")
  add_week_column(table, "Vegan", list(map(lambda m: m.vegan, menu)))
  add_week_column(table, "Vegetarisch", list(map(lambda m: m.veggi, menu)))
  add_week_column(table, "Fleisch", list(map(lambda m: m.meat, menu)))
  add_week_column(table, "Suppe", list(map(lambda m: m.soup, menu)))
  table.min_width = 12
  table.max_width = 35
  table.max_table_width = get_terminal_width() - 6
  print(table)

def main():
  # input parsing

  do_week = False

  def print_usage():
    print(f"Usage:")
    print(f"  {sys.argv[0]} [day|week]")
    print(f"    Prints the PTB mensa's menu of the day (default) or week.")

  if len(sys.argv) == 2:
    if sys.argv[1] == "day":
      pass
    elif sys.argv[1] == "week":
      do_week = True
    else:
      print(f"Unknown argument: {sys.argv[1]}")
      print_usage()
      exit(-1)
  elif len(sys.argv) > 2:
    print(f"Too many arguments!")
    print_usage()
    exit(-1)


  # implementation

  if do_week:
    print_week()
  else:
    print_today()

if __name__ == "__main__":
  main()
