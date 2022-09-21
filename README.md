# PTB Mensa (Berlin) Menu

This python package parses the [PTB Mensa's (in Berlin) menu](https://www.cc-kuehnel.de/wochenspeiseplan) and provides it as machine readable python structures.

The challenge here is, that the menu is only provided as an image, and therefore needs to be processed with OCR.

## Installation

You can install the module directly with pip:

```bash
$ pip install git+https://github.com/hnj2/ptb-mensa.git
```

You can also clone and install the module:

```bash
$ git clone https://github.com/hnj2/ptb-mensa.git
$ cd ptb-mensa
$ pip install -e .
```

## Usage

The acompanying cli can be used as follows:

```bash
$ ptb-mensa help
Unknown argument: help
Usage:
  ptb-mensa [day|week]
    Prints the PTB mensa's menu of the day (default) or week.
$ ptb-mensa day
+----------------------------------------------------------------------------------------------------------------------------------+
|                                                PTB Mensa Menu Mittwoch 21.09.2022                                                |
+--------+--------------------------------+--------------------------------+--------------------------------+----------------------+
|        |             Vegan              |          Vegetarisch           |            Fleisch             |        Suppe         |
+--------+--------------------------------+--------------------------------+--------------------------------+----------------------+
|   Menu |     Sellerieschnitzel mit      |         Pumpernickel-          |   Kalbleber Berliner Art mit   |  Brokkolicremesuppe  |
|        | Süßkartoffelpüree_ Gurkensalat |     Frischkäsebällchen auf     |   Apfel, Zwiebeln und Püree    |                      |
|        |      und Schwarzen Bohnen      |  Blaubeersoße, Kräuterbrot &   |                                |                      |
|        |                                |       Wildkräuter salat        |                                |                      |
|  Preis |             5,00 €             |             5,00 €             |             6,50 €             |  klein 2,80 € groß   |
|        |                                |                                |                                |        3,80 €        |
|  Extra |              None              |              G/AJ              |            G/Aa /€             |          V           |
+--------+--------------------------------+--------------------------------+--------------------------------+----------------------+
```

But the module can also be used directly in python:

```ipython
In [1]: import ptb_mensa

In [2]: ptb_mensa.menu()
Out[2]: DayMenu(vegan=Menu(description='Sellerieschnitzel mit Süßkartoffelpüree_ Gurkensalat und Schwarzen Bohnen', price='5,00 €', extra=None), veggi=Menu(description='Pumpernickel-Frischkäsebällchen auf Blaubeersoße, Kräuterbrot & Wildkräuter salat', price='5,00 €', extra='G/AJ'), meat=Menu(description='Kalbleber Berliner Art mit Apfel, Zwiebeln und Püree', price='6,50 €', extra='G/Aa /€'), soup=Menu(description='Brokkolicremesuppe', price='klein 2,80 € groß 3,80 €', extra='V'))
```

## Notes

I am not affiliated in any way with the PTB mensa!

