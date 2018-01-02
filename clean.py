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

num_re = r'[0-9]+(\.[0-9]+)?'
unit_re = r'(--|%|mcg|mg|g|ui|ng|ml)'

drug_name_re = r'(?P<name>[a-z][a-z0-9]*( [a-z][a-z0-9]*)*)'
drug_unit_re = r'(?P<unit>%s%s(/(%s)?%s)?)(,(?P<unit_extra>%s%s(/(%s)?%s)?))?' % ((num_re, unit_re) * 4)
drug_dose_re = r'(?P<dose>%su/(%s)?[a-z])' % ((num_re,) * 2)

drug_pattern = re.compile(r'^%s( %s)?( %s)?$' % (drug_name_re, drug_unit_re, drug_dose_re))

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

def read_csvfile(name):
  csvfile = open(name)
  reader = csv.reader(csvfile)
  reader.next()
  matrix = [r for r in reader]
  csvfile.close()
  return matrix

def replace(val, old, new, params=[], out=False):

  def repl(match):
    groups = ['' if i is None else i for i in [match.group(k) for k in params]]
    return new % tuple(groups)

  regex = re.compile(old)
  value = re.sub(regex, repl, val)
  value = re.sub(regex, repl, value)

  if out and value != val:
    print val + ' --> ' + value
  return value

def parse_float(val):
  return float("%.2f" % (float(val),))

def clean_drug(drug):
  drug = ' '.join(filter(lambda s: len(s) > 0, drug.split(' ')))
  drug = drug.lower()

  drug = replace(drug, r'(Á|á|Ä|ä)', 'a')
  drug = replace(drug, r'(É|é)', 'e')
  drug = replace(drug, r'(Í|í)', 'i')
  drug = replace(drug, r'(Ó|ó)', 'o')
  drug = replace(drug, r'(Ú|ú)', 'u')
  drug = replace(drug, r'(\(|_|\))', '')
  drug = replace(drug, r'o\.', '0.')
  drug = replace(drug, r' -', '-')
  drug = replace(drug, r'\buno\b', '1')
  drug = replace(drug, r'\bdos\b', '2')
  drug = replace(drug, r'(?P<a>[0-9]) ?(cucha|inhal)[a-z]+', '%su', ['a'])
  drug = replace(drug, r' ?%su/?$' % (num_re,), '')
  drug = replace(drug, r'-- 1$', '--')
  drug = replace(drug, r'u cada (?P<a>%s) ?(?P<b>[a-z]).+$' % (num_re,), 'u/%s%s', ['a', 'b'])
  drug = replace(drug, r'u/(?P<a>%s)?(?P<b>[a-z]).+$' % (num_re,), 'u/%s%s', ['a', 'b'])
  drug = replace(drug, r' 0 ?(?P<a>[0-9])', '0.%s', ['a'])
  drug = replace(drug, r'^0(?P<a>[a-z])', 'o%s', ['a'])
  drug = replace(drug, r'(?P<a>[a-z]+)(?P<b>[0-9])', '%s %s', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[a-z]) ?(-|\.) ?(?P<b>[a-z0-9])', '%s %s', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9])[ a-z]*al (?P<b>(m|d|s)).*', '%su/%s', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]) (?P<b>%s)u' % (num_re,), '%s-- %su', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>[0-9]+)--', '%s.%s--', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9])/(?P<b>%s)--' % (num_re,), '%s--/%s--', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[a-z]{2,})/(?P<b>[a-z]{2,})', '%s %s', ['a', 'b'])
  drug = replace(drug, r' ?m[a-z]*c[a-z]*g[a-z]*', 'mcg')
  drug = replace(drug, r'\.(?![0-9])', '')
  drug = replace(drug, r'b 12', 'b12')
  drug = replace(drug, r'\b(?P<a>[a-z]+) (?P<b>%s)$' % (num_re,), '%s %s--', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]) ?gr?\b', '%sg', ['a'])
  drug = replace(drug, r'(?P<a>[0-9])--( |\+)(?P<b>%s)--' % (num_re,), '%s--/%s--', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]) ?m\b', '%smg', ['a'])
  drug = replace(drug, r'u (?P<a>%s)(?P<b>[a-z])$' % (num_re,), 'u/%s%s', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>[0-9]+) (?P<c>[0-9]+)', '%s--/%s.%s--', ['a', 'b', 'c'])
  drug = replace(drug, r'durante (?P<a>[0-9]+) h.*', '1u/%sh', ['a'])
  drug = replace(drug, r'(?P<a>[0-9])[ a-z]+d[a-z]*ria', '%su/d', ['a'])
  drug = replace(drug, r'--/(?P<a>[0-9]+)h.*', '-- 1u/%sh', ['a'])
  drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>[a-z]{4,})', '%s %s--', ['b', 'a'])
  drug = replace(drug, r'(?P<a>[0-9]+)-- (?P<b>[a-z]+)', '%s %s--', ['b', 'a'])
  drug = replace(drug, r'(?P<a>[0-9]+)/(?P<b>[a-z])$', '%su/%s', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]) (?P<b>[a-z]{2})$', '%s%s', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>%s)(?P<c>(--|mcg))' % (num_re,), '%s--/%s%s', ['a', 'b', 'c'])
  drug = replace(drug, r'(?P<a>[0-9]+) 1/2', '%s.5--', ['a'])
  drug = replace(drug, r'(?P<a>[a-z]+) 1/2', '%s 0.5--', ['a'])
  drug = replace(drug, r'3/4', '0.75')
  drug = replace(drug, r'(?P<a>[0-9])-- (?P<b>[0-9]+) (?P<c>[0-9]+)', '%s--/%s.%s--', ['a', 'b', 'c'])
  drug = replace(drug, r'(?P<a>[0-9])-- ñ(?P<b>[0-9])u/', '%s-- %su/', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>[0-9]+)mg', '%s.%smg', ['a', 'b'])
  drug = replace(drug, r'-- (?P<a>[0-9]+)mg', '--/%smg', ['a'])
  drug = replace(drug, r'(?P<a>[0-9]+)--/(?P<b>[0-9]+)$', '%s--/%s--', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9]+)-(?P<b>[0-9]+)--', '%s--/%s--', ['a', 'b'])
  drug = replace(drug, r'(?P<a>[0-9])oo--', '%s00--', ['a'])
  drug = replace(drug, r'(?P<a>[0-9]+)(--)? y (?P<b>[0-9]+)(--)?', '%s--,%s--', ['a', 'b'])
  drug = replace(drug, r'^(?P<a>[a-z]+) (?P<b>[0-9]+)(fa)? [0-9]+$', '%s %s--', ['a', 'b'])

  return drug

def build_drug(drug):
  drug = clean_drug(drug)
  match = drug_pattern.search(drug)

  name = match.group('name')
  unit = [u for u in [match.group('unit'), match.group('unit_extra')] if u is not None]
  dose = match.group('dose')

  return dict(name=name, unit=unit, dose=dose)

def clean_kidney_fail(key, val):
  return (key, None if val == '' else parse_kidney_fail(key, parse_float(val)))

def parse_kidney_fail(key, val):

  if key == 'height':
    val = parse_float(val / 0.39370)

  if key == 'kidney_failure':
    val = False if val < 1 else True

  if key == 'weight':
    val = parse_float(val / 2.2046)

  return val

def build_kidney_fail(values):
  patient = dict(clean_kidney_fail(x, y) for x, y in zip(patient_info, values))

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

  if None in [patient[k] for k in ['triglycerides', 'cbc']]:
    print [patient[k] for k in ['triglycerides', 'cbc']]

  return patient

def export_json(data, filename):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=2, separators=(',', ': '), sort_keys=True)

# =======================================================================================
# MAIN
# =======================================================================================

patients = read_csvfile('drugs.csv')
patients = [filter(lambda col: col not in ['N', 'NA'], row) for row in patients]
patients = dict((int(row[0]), map(build_drug, row[1:])) for row in patients)

export_json(patients, 'drugs.json')

patients = read_csvfile('kidney-fail.csv')
patients = dict((int(row[0]), build_kidney_fail(row[1:])) for row in patients)

export_json(patients, 'kidney-fail.json')
