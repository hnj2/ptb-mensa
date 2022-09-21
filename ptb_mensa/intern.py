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

import re
import io
import sys
from contextlib import redirect_stderr
from dataclasses import dataclass
from typing import Union,Dict
from datetime import datetime

import requests
from PIL import Image
import numpy
import easyocr


# retrieving the menu image

BASE_URL = "https://www.cc-kuehnel.de"
MENU_URL = f"{BASE_URL}/wochenspeiseplan"

def get_webtext():
  ans = requests.get(MENU_URL)
  ans.raise_for_status()
  return ans.text

IMG_SRC_RE = re.compile(r"<img[^>]+src=\"([^\"]+)\"[^>]*>")

def get_menu_url():
  matches = IMG_SRC_RE.findall(get_webtext())
  return BASE_URL + matches[1]

def get_menu_image():
  im_re = requests.get(get_menu_url())
  return Image.open(io.BytesIO(im_re.content))

# splitting menu into table-tiles

border_color = (139, 175, 223)

def get_border_color_row_col_counts(image):
  im = numpy.array(image)
  dist_3d = im - border_color
  dist = numpy.sqrt((dist_3d*dist_3d).sum(axis=-1))
  border = dist < 50
  return border.sum(axis=1), border.sum(axis=0)

def get_row_col_midpoints(arr):
  thresh = (arr.max()*9 + arr.min()) / 10
  barr = arr > thresh

  result = []
  start = None
  for (i, is_high) in enumerate(barr):
    if start is None:
      if is_high:
        start = i
    else:
      if not is_high:
        result.append(int((i+start)/2))
        start = None

  return result

def get_menu_tiles():
  img = get_menu_image()
  rows, cols = get_border_color_row_col_counts(img)
  rows = get_row_col_midpoints(rows)
  cols = get_row_col_midpoints(cols)

  results = []

  for (r_s, r_e) in zip(rows[:-1], rows[1:]):
    results_col = []
    for (c_s, c_e) in zip(cols[:-1], cols[1:]):
      results_col.append(img.crop((c_s, r_s, c_e, r_e)))
    results.append(results_col)
  
  return results

# parsing images to text

__OCR_READER__ = None

def ocr(img):
  global __OCR_READER__
  if __OCR_READER__ is None:
    with redirect_stderr(io.StringIO()):
      __OCR_READER__ = easyocr.Reader(["de"])
  return __OCR_READER__.readtext(numpy.array(img))

def img_to_text(img):
  result = None
  for t in ocr(img):
    text = t[1]
    if not result:
      result = text
    elif result[-1] == "-":
      result = result[:-1] + text
    else:
      result += " " + text
  return result

def img_to_menu_attributes(img):
  texts = ocr(img)

  texts.sort(key=lambda t: t[0][0][0])

  sepa = 10
  thresh = sepa
  pos = 0

  first = None
  while texts[pos][0][0][0] < thresh:
    if first:
      first += " " + texts[pos][1]
    else:
      first = texts[pos][1]
    thresh = texts[pos][0][1][0] + sepa
    pos += 1
  
  second = None
  for t in texts[pos:]:
    if second:
      second += " " + t[1]
    else:
      second = t[1]

  return first, second

# creating the menu structure

@dataclass
class Menu:
  description : str
  price : str
  extra : str

@dataclass
class DayMenu:
  vegan : Menu
  veggi : Menu
  meat : Menu
  soup : Menu

def get_day_menus(description_images, attribute_images):
  descriptions = list(map(img_to_text, description_images))
  attributes = list(map(img_to_menu_attributes, attribute_images))
  return DayMenu(*[
    Menu(descriptions[i], attributes[i][1], attributes[i][0])
    for i in range(4)
  ])

def get_week_menus():
  tiles_img = get_menu_tiles()
  assert len(tiles_img) % 2 == 1

  #menu_names = list(map(img_to_text, tiles_img[0][1:]))

  results = list()
  dates = list()

  for start in range(1, len(tiles_img), 2):
    first_line = tiles_img[start]
    second_line = tiles_img[start+1]

    date = img_to_text(first_line[0])

    day_menus = get_day_menus(tiles_img[start][1:], tiles_img[start+1][1:])

    results.append(day_menus)
    dates.append(date)

  return results, dates
