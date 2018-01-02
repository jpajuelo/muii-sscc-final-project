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
  'bun',
  'monocytes',
  'granulocytes',
  'eosinophils',
  'basophils',
  'blood_sugar_level',
  'platelet_count',
  'mean_platelet_volume',
  'leukocytes',
  'trgld',
  'tflr',
  'kidney_failure'
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

def parse_float(val):
  return float("%.2f" % (float(val),))

def clean(key, val):
  return (key, None if val == '' else parse(key, parse_float(val)))

def parse(key, val):

  if key == 'height':
    val = parse_float(val / 0.39370)

  if key == 'kidney_failure':
    val = False if val < 1 else True

  if key == 'weight':
    val = parse_float(val / 2.2046)

  return val

def build(values):
  patient = dict(clean(x, y) for x, y in zip(patient_info, values))

  wbc_k = ['basophils', 'eosinophils', 'monocytes']
  wbc_v = [patient.pop(k) for k in wbc_k]

  patient.update({
    'bmi': parse_float(patient.pop('weight') / (patient.pop('height') * 0.01) ** 2),
    'wbc_count': None if None in wbc_v else dict(zip(wbc_k, wbc_v))
  })

  return patient

# =======================================================================================
# MAIN
# =======================================================================================

patients = read_csv('kidney-fail.csv')
patients = dict((int(row[0]), build(row[1:])) for row in patients)

exportJSON(patients, 'kidney-fail.json')
