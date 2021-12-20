from urllib import request, parse
import base64
import os
import random

CONFIG_DIR=os.path.expanduser('~/.nato-checker')

CONFIG_FILE_PATH = f'{CONFIG_DIR}/config'
CURRENT_REQUEST_FILE_PATH = f'{CONFIG_DIR}/current'
NEXT_REQUESTS_FILE_PATH = f'{CONFIG_DIR}/next'

ANSWERS = {
  'a': 'alpha',
  '0': 'zero',
}

ACCOUNT_SID = AUTH_SID = AUTH_KEY = None

with open(CONFIG_FILE_PATH, encoding='utf-8') as f:
  for line in f:
    line = line.strip()

    if line[0] == '#':
      continue

    line = line.split('=')
    assert len(line) == 2

    if line[0] == 'ACCOUNT_SID':
      ACCOUNT_SID = line[1]
    elif line[0] == 'AUTH_SID':
      AUTH_SID = line[1]
    elif line[0] == 'AUTH_KEY':
      AUTH_KEY = line[1]
    else:
      raise ValueError(f'wat is {line[0]}')

assert ACCOUNT_SID
assert AUTH_SID
assert AUTH_KEY

current_letter = None
try:
  with open(CURRENT_REQUEST_FILE_PATH, encoding='utf-8') as f:
    current_letter = f.read(1)
  assert ('a' <= current_letter <= 'z') or ('0' <= current_letter <= '9')
except:
  pass

next_letters = ''
try:
  with open(NEXT_REQUESTS_FILE_PATH, encoding='utf-8') as f:
    next_letters = f.read(len(ANSWERS))
except:
  pass

if len(next_letters) == 0:
  next_letters = ''.join(random.sample(list(ANSWERS.keys()), len(ANSWERS)))

assert len(next_letters) > 0

next_letter = next_letters[0]
next_letters = next_letters[1:]

assert next_letter in ANSWERS

with open(NEXT_REQUESTS_FILE_PATH, 'w', encoding='utf-8') as f:
  f.write(next_letters)

with open(CURRENT_REQUEST_FILE_PATH, 'w', encoding='utf-8') as f:
  f.write(next_letter)

if current_letter:
  message_body = f'bzzzt! {current_letter} is {ANSWERS[current_letter]}. {next_letter}?'
else:
  message_body = next_letter


r = request.Request(
  f'https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json',
  parse.urlencode({
    'Body': message_body,
    'From': '+19542660248',
    'To': '+13472660248',
  }).encode(),
  {
    'Authorization': f'Basic {base64.b64encode(f"{AUTH_SID}:{AUTH_KEY}".encode("utf-8")).decode("utf-8")}',
  }
)

print(request.urlopen(r).read().decode('utf-8'))
