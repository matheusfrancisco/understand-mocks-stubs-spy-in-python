from urllib.request import urlopen
from urllib.error import HTTPError
import logging
import os

def search_book(book):
  r = make_request_no_try_catch(make_data_to_request(book), 10)
  return r


def make_data_to_request(request):
    return request

def make_request_no_try_catch(url, timeout):
  with urlopen(url, timeout) as response:
    result = response.read().decode("utf-8")
  return result

def make_request(url, timeout):
  try:
    with urlopen(url, timeout) as response:
      result = response.read().decode("utf-8")
  except HTTPError as e:
    logging.exception(f"Ao acessar {url}: {e}")
  else:
    return result

def write_file(file_dir, content):
  path_dir = os.path.dirname(file_dir)
  try:
    os.makedirs(path_dir)
  except OSError:
    logging.exception(f"não foi possivel criar diretório {path_dir}")
  try:
    with open(file_dir, 'w') as fp:
      fp.write(content)
  except OSError as e:
    logging.exception(f"não foi possível criar arquivo {file_dir}")
