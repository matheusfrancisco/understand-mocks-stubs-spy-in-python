from urllib.request import urlopen, Request
from urllib.error import HTTPError
import logging
import os
from urllib.parse import urlencode
import json
from math import ceil

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



class Search:
    """
    Classe Search
    Storage data to search text
    - autor, titulo e livro
    - pagina
    - url
    - dados_para_requisicao
    """

    def __init__(self, author=None, title=None, book=None):
        self._author = author
        self._title = title
        self._book = book
        self._page = 0
        self._data_to_request = None
        self._url = "https://buscarlivros"

    @property
    def page(self):
        return self._page

    @property
    def data_to_request(self):
        """
        Retorna um dicionário com os dados de Consulta
        """
        if not self._data_to_request:
            self._data_to_request = {}
            if self._book:
                self._data_to_request = {"q": self._book}
            else:
                if self._author:
                    self._data_to_request["author"] = self._author
                if self._title:
                    self._data_to_request["title"] = self._title
        return self._data_to_request

    @property
    def seguinte(self):
        data_to_request = self.data_to_request
        self._page += 1
        data_to_request["page"] = self._page
        req = Request(self._url, data_to_request)
        if req.data:
            return req.full_url + "?" + urlencode(req.data)

class Response:
    """
    Conteúdo da página em formato JSON
    """

    # quantidade de documentos max esperado por página
    qtd_docs_por_pagina = 50

    def __init__(self, conteudo):
        # conteudo da pagina pura
        self._conteudo = conteudo
        # conteudo processado, formato dicionário
        self._dados = None

    @property
    def conteudo(self):
        return self._conteudo

    @property
    def dados(self):
        if not self._dados:
            try:
                j = json.loads(self.conteudo)
            except TypeError as e:
                logging.exception(
                    "Resultado da consulta '%s': tipo inválido. " % self.conteudo
                )
            except json.JSONDecodeError as e:
                logging.exception(
                    "Resultado da consulta '%s': JSON inválido. " % self.conteudo
                )
            else:
                self._dados = j
        return self._dados

    @property
    def documentos(self):
        # documentos retornados na pagina
        return self.dados.get("docs", [])

    @property
    def total_de_paginas(self):
        # total de paginas, todos os resultados
        if len(self.documentos):
            return ceil(self.dados.get("num_docs", 0) / self.qtd_docs_por_pagina)
        return 0


def download_book(arquivo, author=None, title=None, book=None):
    search = Search(author, title, book)
    total_pages = 1
    i = 0
    while True:
      result = make_request(search.seguinte, 10)
      if result:
        response = Response(result)
        total_pages = response.total_de_paginas
        write_file(arquivo[i], result)
      if search.page == 1:
        total_pages = 2
      if search.page == total_pages:
        break
      i += 1
