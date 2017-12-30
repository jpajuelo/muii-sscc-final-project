# -*- coding: utf-8 -*-

# =======================================================================================
# DEPENDENCIES
# =======================================================================================

import csv
import json
import re

# =======================================================================================
# VARS
# =======================================================================================

patient_info = [
  'height',
  'weight',
  'urea',
  'monocytes',
  'granulocytes',
  'eosinophils',
  'basophils',
  'glucose',
  'platelets',
  'mean_platelet_volume',
  'leukocytes',
  'trgld',
  'tflr',
  'kidney failure'
]

# =======================================================================================
# METHODS
# =======================================================================================

def read_csv(filename):
  values = []
  with open(filename, 'rb') as csvfile:
    values = [row for i, row in enumerate(csv.reader(csvfile)) if i != 0]
  return values

def exportJSON(data, filename):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=2, separators=(',', ': '), sort_keys=True)

def format_float(val):
  return float("%.2f" % (float(val),))

def clean(key, val):
  val = None if val == '' else format_float(val)

  if key == 'kidney failure':
    val = False if val < 1 else True

  return (key, val)

# =======================================================================================
# MAIN
# =======================================================================================

patients = read_csv('kidney-fail.csv')
patients = dict((int(row[0]), dict(clean(x, y) for x, y in zip(patient_info, row[1:]))) for row in patients)

exportJSON(patients, 'kidney-fail.json')
