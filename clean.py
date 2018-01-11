# -*- coding: utf-8 -*-

# =======================================================================================
# DEPENDENCIES
# =======================================================================================

import csv
import json
import re

from itertools import groupby

# =======================================================================================
# CONSTANTS
# =======================================================================================

NUM_RE = r'[0-9]+(\.[0-9]+)?'
UNIT_RE = r'(--|%|mcg|mg|g|ui|ng|ml)'
NAME_RE = r'[a-z][a-z0-9]*( [a-z][a-z0-9]*)*'

DRUG_NAME_RE = r'(?P<name>%s)(,(?P<name_extra>%s))?' % ((NAME_RE,) * 2)
DRUG_UNIT_RE = r'((?P<unit>%s)%s(/(%s)?%s)?)(,((?P<unit_extra>%s)%s(/(%s)?%s)?))?' % ((NUM_RE, UNIT_RE) * 4)
DRUG_DOSE_RE = r'(?P<dose>(?P<dose_unit>%s)u/(?P<dose_time_v>%s)(?P<dose_time_k>[a-z]))' % ((NUM_RE,) * 2)

DRUG_PATTERN = re.compile(r'^%s( %s)?( %s)?$' % (DRUG_NAME_RE, DRUG_UNIT_RE, DRUG_DOSE_RE))

PATIENT_K = [
  'height',
  'weight',
  'blood_urea_nitrogen',
  'monocyte',
  'neutrophil',
  'eosinophil',
  'basophil',
  'blood_glucose',
  'platelet',
  'mean_platelet_volume',
  'white_blood_cell',
  'triglyceride',
  'tflr',
  'kidney_failure'
]

WORDS_TO_REMOVE = [
  'accuhaler',
  'aerosol',
  'ampollas',
  'capsulas',
  'gel',
  'gotas',
  'inhalador',
  'jarabe',
  'lagrimas',
  'masticable',
  'msd',
  'neo',
  'plus',
  'parches',
  'polvo para inhalacion',
  'sobres',
  'turbuhaler',
  'turboinhale',
  'vial'
]

# =======================================================================================
# HELPERS
# =======================================================================================

def clean_csvfile(name, clean):
  return dict((int(r[0]), clean(r[1:])) for r in read_csvfile(name))

def export_json(data, name):
  with open('%s.json' % (name,), 'w') as outfile:
    json.dump(data, outfile, indent=2, separators=(',', ': '), sort_keys=True)

def read_csvfile(name):
  csvfile = open('csvfiles/%s.csv' % (name,))
  reader = csv.reader(csvfile)
  reader.next()
  matrix = [r for r in reader]
  csvfile.close()
  return matrix

def replace(val, old, new, params=[], debug=False):

  def repl(match):
    groups = ['' if i is None else i for i in [match.group(k) for k in params]]
    return new % tuple(groups)

  regex = re.compile(old)
  value = re.sub(regex, repl, val)
  value = re.sub(regex, repl, value)

  if debug and value != val:
    print '%s // %s' % (val, value)
  return value

def parse_float(val):
  return None if val is None else float("%.2f" % (float(val),))

# =======================================================================================
# METHODS
# =======================================================================================

def clean_patient(patient_v):
  patient = dict((k, None if v == '' else parse_float(v)) for k, v in zip(PATIENT_K, patient_v))

  """
  bmp_k = ['blood_glucose', 'blood_urea_nitrogen', 'triglyceride']
  bmp_v = [patient.pop(k) for k in bmp_k]

  wbc_k = ['basophil', 'eosinophil', 'monocyte', 'neutrophil']
  wbc_v = [patient.pop(k) for k in wbc_k]

  bc_k = ['mean_platelet_volume', 'platelet', 'white_blood_cell']
  bc_v = [patient.pop(k) for k in bc_k]

  bc_type = None if None in bc_v else dict(zip(bc_k, bc_v))

  if bc_type is not None:
    bc_type.update({
      'white_blood_cell_type': None if None in wbc_v else dict(zip(wbc_k, wbc_v))
    })
  """

  patient.update({
    #'basic_metalobic_panel': None if None in bmp_v else dict(zip(bmp_k, bmp_v)),
    'blood_mass_index': parse_float(703 * (patient.pop('weight') / patient.pop('height') ** 2)),
    #'blood_cell_type': bc_type,
    'kidney_failure': int(patient.get('kidney_failure')),
  })

  return patient

def clean_patient_drugs(patient_drugs):
  cleaned = []

  for drug in patient_drugs:
    drug = ' '.join(filter(lambda s: len(s) > 0, drug.split(' ')))
    drug = drug.lower()

    if drug in ['n', 'na']:
      continue

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
    drug = replace(drug, r' ?%su/?$' % (NUM_RE,), '')
    drug = replace(drug, r'-- 1$', '--')
    drug = replace(drug, r'u cada (?P<a>%s) ?(?P<b>[a-z]).+$' % (NUM_RE,), 'u/%s%s', ['a', 'b'])
    drug = replace(drug, r'u/(?P<a>%s)?(?P<b>[a-z]).+$' % (NUM_RE,), 'u/%s%s', ['a', 'b'])
    drug = replace(drug, r' 0 ?(?P<a>[0-9])', ' 0.%s', ['a'])
    drug = replace(drug, r'^0(?P<a>[a-z])', 'o%s', ['a'])
    drug = replace(drug, r'(?P<a>[a-z]+)(?P<b>[0-9])', '%s %s', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[a-z]) ?(-|\.) ?(?P<b>[a-z])', '%s%s', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[a-z]) ?(-|\.) ?(?P<b>[0-9])', '%s %s', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9])[ a-z]*al (?P<b>(m|d|s)).*', '%su/%s', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9]) (?P<b>%s)u' % (NUM_RE,), '%s-- %su', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>[0-9]+)--', '%s.%s--', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9])/(?P<b>%s)--' % (NUM_RE,), '%s--/%s--', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[a-z]{2,})/(?P<b>[a-z]{2,})', '%s %s', ['a', 'b'])
    drug = replace(drug, r' ?m[a-z]*c[a-z]*g[a-z]*', 'mcg')
    drug = replace(drug, r'\.(?![0-9])', '')
    drug = replace(drug, r'b 12', 'b12')
    drug = replace(drug, r'\b(?P<a>[a-z]+) (?P<b>%s)$' % (NUM_RE,), '%s %s--', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9]) ?gr?\b', '%sg', ['a'])
    drug = replace(drug, r'(?P<a>[0-9])--( |\+)(?P<b>%s)--' % (NUM_RE,), '%s--/%s--', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9]) ?m\b', '%smg', ['a'])
    drug = replace(drug, r'u (?P<a>%s)(?P<b>[a-z])$' % (NUM_RE,), 'u/%s%s', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>[0-9]+) (?P<c>[0-9]+)', '%s--/%s.%s--', ['a', 'b', 'c'])
    drug = replace(drug, r'durante (?P<a>[0-9]+) h.*', '1u/%sh', ['a'])
    drug = replace(drug, r'(?P<a>[0-9])[ a-z]+d[a-z]*ria', '%su/d', ['a'])
    drug = replace(drug, r'--/(?P<a>[0-9]+)h.*', '-- 1u/%sh', ['a'])
    drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>[a-z]{4,})', '%s %s--', ['b', 'a'])
    drug = replace(drug, r'(?P<a>[0-9]+)-- (?P<b>[a-z]+)', '%s %s--', ['b', 'a'])
    drug = replace(drug, r'(?P<a>[0-9]+)/(?P<b>[a-z])$', '%su/%s', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9]) (?P<b>[a-z]{2})$', '%s%s', ['a', 'b'])
    drug = replace(drug, r'(?P<a>[0-9]+) (?P<b>%s)(?P<c>(--|mcg))' % (NUM_RE,), '%s--/%s%s', ['a', 'b', 'c'])
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
    drug = replace(drug, r'u/(?P<a>[a-z])$', 'u/1%s', ['a'])
    drug = replace(drug, r'^(?P<a>[a-z]+( [a-z]+)*) y (?P<b>[a-z]+( [a-z]+)*)', '%s,%s', ['a', 'b'])
    drug = replace(drug, r' 0--', '')
    drug = replace(drug, r' ?f[a-z]+rte( [a-z]+)?', ' forte')
    drug = replace(drug, r' reta[a-z]+', ' retard')
    drug = replace(drug, r'^neo (?P<a>[a-z]+)', '%s neo', ['a'])
    drug = replace(drug, r'^cod (?P<a>[a-z]+)', '%s codeina', ['a'])
    drug = replace(drug, r' neo [a-z]+', ' neo')
    drug = replace(drug, r' l\b', ' flas')
    drug = replace(drug, r'(?P<a>[a-z]+) ?plus', '%s plus', ['a'])
    drug = replace(drug, r'^(?P<a>[a-z]{,4}) (?P<b>[a-z]+)', '%s%s', ['a', 'b'])
    drug = replace(drug, r' (%s)\b' % '|'.join(WORDS_TO_REMOVE), '')

    match = DRUG_PATTERN.search(drug)

    name = match.group('name')
    unit = match.group('unit')
    dose_unit = match.group('dose_unit')
    dose_time = (match.group('dose_time_k'), match.group('dose_time_v'))

    cleaned.append(create_drug(name, unit, dose_unit, dose_time))

    name_extra = match.group('name_extra')

    if name_extra is not None:
      cleaned.append(create_drug(name_extra, unit, dose_unit, dose_time))

    unit_extra = match.group('unit_extra')

    if unit_extra is not None:
      cleaned.append(create_drug(name, unit_extra, dose_unit, dose_time))

  return cleaned

def parse_dose_time(dose_time):
  if None in dose_time:
    return None

  k, v = dose_time

  v = int(v)

  if k == 'd':
    return v * 24

  if k == 's':
    return v * 7 * 24

  if k == 'm':
    return v * 30 * 24

  return v

def create_drug(name, unit, dose_unit, dose_time):
  dose_k = ['unit', 'time']
  dose_v = [parse_float(dose_unit), parse_dose_time(dose_time)]

  return {
    'name': name,
    'unit': parse_float(unit),
    'dose': None if None in dose_v else dict(zip(dose_k, dose_v))
  }

def create_patterns(val):
  result = []

  for i in range(1, len(val)):
    chars = list(val)

    if chars[-1] in ['l', 'r']:
      chars[-1] = '(l|r)'

    chars = ['(i|y)' if c in ['y', 'i'] else c for c in chars]
    chars = ['h?' if c in ['h'] else c for c in chars]
    chars = ['(k|qu)' if c in ['k'] else c for c in chars]
    chars = ['(c|z)' if c in ['z', 'c'] else c for c in chars]
    chars = ['(x|s)' if c in ['x', 's'] else c for c in chars]
    chars = ['(m|n)' if c in ['m', 'n'] else c for c in chars]
    chars = ['(v|u)' if c in ['v', 'u'] else c for c in chars]
    chars = ['(a|e)' if c in ['a', 'e'] else c for c in chars]
    chars = [' ?' if c in [' '] else c for c in chars]

    chars[i] = chars[i] + r'[a-z]?'

    if i + 1 < len(chars):
      del chars[i + 1]

    result.append(re.compile(r'^' + ''.join(chars) + r'$'))

  return result

# =======================================================================================
# MAIN
# =======================================================================================

patient = clean_csvfile('patient', clean_patient)
patient_drugs = clean_csvfile('patient_drugs', clean_patient_drugs)

drug_names = [d.get('name') for p_i, p_d in patient_drugs.items() for d in p_d]
drug_names = [(k, len(list(g))) for k, g in groupby(sorted(drug_names))]

result = []

for d_n in drug_names:
  n, c = d_n
  names = [n]

  for p in create_patterns(n):
    for new_d_n in drug_names:
      new_n, new_c = new_d_n
      if p.search(new_n):
        if new_c > c:
          n = new_n
          c = new_c
        names.append(new_n)

  names = list(set(names))

  if len(names) > 1:
    result.append(', '.join(sorted(names)))

    for p_i, p_d in patient_drugs.items():
      for d in p_d:
        if d.get('name') in names:
          d['name'] = n

#print '\n'.join(sorted(set(result)))

for p_id, p_drugs in patient_drugs.items():
  if p_id in patient:
    patient.get(p_id).update({
      'drugs': p_drugs
    })

export_json(patient, 'patient')

with open('outfiles/patient.csv', 'w') as csvfile:
  fieldnames = [
    'patient_id',
    'basophil',
    'blood_glucose',
    'blood_urea_nitrogen',
    'eosinophil',
    'kidney_failure',
    'mean_platelet_volume',
    'monocyte',
    'neutrophil',
    'platelet',
    'triglyceride',
    'tflr',
    'white_blood_cell',
  ]

  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  for p_id, p_info in patient.items():
    writer.writerow({
      'patient_id': p_id,
      'basophil': p_info.get('basophil'),
      'blood_glucose': p_info.get('blood_glucose'),
      'blood_urea_nitrogen': p_info.get('blood_urea_nitrogen'),
      'eosinophil': p_info.get('eosinophil'),
      'kidney_failure': p_info.get('kidney_failure'),
      'mean_platelet_volume': p_info.get('mean_platelet_volume'),
      'monocyte': p_info.get('monocyte'),
      'neutrophil': p_info.get('neutrophil'),
      'platelet': p_info.get('platelet'),
      'triglyceride': p_info.get('triglyceride'),
      'tflr': p_info.get('tflr'),
      'white_blood_cell': p_info.get('white_blood_cell'),
    })

drug_cleaned = [d.get('name') for p_i, p_d in patient_drugs.items() for d in p_d]
drug_cleaned = [(k, len(list(g))) for k, g in groupby(sorted(drug_cleaned))]

drug_removed = [(k, v) for k, v in drug_cleaned if v == 1]

with open('drug_cleaned.txt', 'w') as outfile:
  print >> outfile, '\n'.join(sorted(set(['%s %s' % (k,v) for k, v in drug_cleaned])))

with open('drug_removed.txt', 'w') as outfile:
  print >> outfile, '\n'.join(sorted(set(['%s %s' % (k,v) for k, v in drug_removed])))
