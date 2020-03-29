import pytest
from unittest.mock import patch, mock_open, Mock, MagicMock
from library.books import write_file

class DubleLogging():
  def __init__(self):
    self._messagens = []

  def exception(self, message):
    self._messagens.append(message)

  @property
  def messages(self):
    return self._messagens

def d_makedirs(dis):
  raise OSError(f"não foi possivel criar diretorio {dis}")

#spy
#registrando o que faz
#funcao captura e armazena as informações geradas
def test_should_create_dir_return_exception_not_is_possible_create_dir():
  file_dir = "/tmp/arquivo"
  content = " books infos"
  duble_logging = DubleLogging()
  with patch("library.books.os.makedirs", d_makedirs):
    with patch("library.books.logging", duble_logging):
      write_file(file_dir, content)
      assert f"não foi possivel criar diretório /tmp" in duble_logging.messages

@patch("library.books.os.makedirs")
@patch("library.books.logging.exception")
@patch("library.books.open", side_effect=OSError())
def test_should_registry_error_when_write_in_file(stub_open, spy_exception, stub_makedirs):
  file_dir = "/bla/arquivo.json"
  write_file(file_dir, "dados")
  spy_exception.assert_called_once_with(f"não foi possível criar arquivo {file_dir}")


class SpyFp:
  def __init__(self):
    self._content = None

  def __enter__(self):
    return self

  def __exit__(self, p1, p2, p3):
    pass

  def write(self, content):
    self._content = content


@patch("library.books.open")
def test_should_call_write(stub_open):
  arq = "/tmp/arquivo"
  content = "content file"
  spy_fp = SpyFp()
  stub_open.return_value = spy_fp

  write_file(arq, content)
  assert spy_fp._content == content


@patch("library.books.open")
def test_should_call_write_1(stub_open):
  arq = "/tmp/arquivo"
  content = "content file"
  spy_fp = MagicMock()
  spy_fp.__enter__.return_value = spy_fp
  spy_fp.__exit__.return_value = None
  stub_open.return_value = spy_fp

  write_file(arq, content)
  spy_fp.write.assert_called_once_with(content)
