#!/usr/bin/env python

from csv import DictReader
from json import dumps as to_json
import fileinput

reader = DictReader(fileinput.input(), dialect='excel-tab')
print to_json([x for x in reader], indent=2)
