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
  'monocyte',
  'neutrophil', # also called 'granulocytes'
  'eosinophil',
  'basophil',
  'blood_sugar_level',
  'plt',
  'mpv',
  'wbc',
  'triglycerides',
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

  cbc_k = ['plt', 'mpv', 'wbc']
  cbc_v = [patient.pop(k) for k in cbc_k]

  wbc_k = ['basophil', 'eosinophil', 'monocyte', 'neutrophil']
  wbc_v = [patient.pop(k) for k in wbc_k]

  cbc = None if None in cbc_v else dict(zip(cbc_k, cbc_v))

  if cbc is not None:
    cbc.update({
      'wbc_report':  None if None in wbc_v else dict(zip(wbc_k, wbc_v))
    })

  patient.update({
    'bmi': parse_float(patient.pop('weight') / (patient.pop('height') * 0.01) ** 2),
    'cbc': cbc
  })

  return patient

# =======================================================================================
# MAIN
# =======================================================================================

patients = read_csv('kidney-fail.csv')
patients = dict((int(row[0]), build(row[1:])) for row in patients)

exportJSON(patients, 'kidney-fail.json')
