import pytest
from library import __version__
from library.books import search_book, make_request, make_request_no_try_catch
from unittest.mock import patch, mock_open, Mock, MagicMock

from urllib.error import HTTPError
"""
Que existe um dublê do tipo Dummy que serve para substituir parâmetros obrigatórios,
mas não são usados na verificação do caso de teste e, por isso, são irrelevantes

Como implementar Dummy sem a biblioteca unittest.mock

Como implementar Dummy com a biblioteca unittest.mock

Que existe um dublê do tipo Stub para fornecer dados fabricados ou comportamentos
esperados para serem usados na verificação do caso de teste

Como usar o dublê Stub para substituir o resultado de uma requisição a uma página da
Internet, sem que a requisição de fato ocorra

Como implementar nosso próprio Stub, sem usar a biblioteca unittest.mock

Como implementar Stub com a biblioteca unittest.mock

Como testar quando exceções são levantadas

Como testar quando quando exceções foram "logadas"
"""

#Stub
#Fornece um dado pré definido fabricado
class StubHTTPResponse:
  def read(self):
    return b""

  def __enter__(self):
    return self

  def __exit__(self, p1, p2, p3):
    pass

def stub_urlopen(url, timeout):
  return StubHTTPResponse()



def test_version():
    assert __version__ == '0.1.0'


@patch("library.books.urlopen", return_value=StubHTTPResponse())
def test_search_books_should_return_string(stub_urlopen):
  result = search_book("Agatha Christie")
  assert type(result) == str


#spy function, verify if called with params
@patch("library.books.urlopen", return_value=StubHTTPResponse())
def test_search_books_should_call_data_request_with_params(stub_urlopen):
  with patch("library.books.make_data_to_request") as spy:
    search_book("Agatha Christie")
    spy.assert_called_once_with("Agatha Christie")


def test_make_request_should_return_type_string():
  with patch("library.books.urlopen", stub_urlopen):
    r = make_request("https://buscarlivros/author=Jk_Rowlings", 100)
  assert type(r) == str

#type mock
#mock que vai retornar uma instancia
def test_make_request_should_return_type_string_1():
  with patch("library.books.urlopen") as mock_urlopen:
    mock_urlopen.return_value = StubHTTPResponse()
    r = make_request("https://buscarlivros/author=Jk_Rowlings", 100)
  assert type(r) == str


def test_make_request_should_return_type_string_2():
  with patch("library.books.urlopen", return_value=StubHTTPResponse()):
    r = make_request("https://buscarlivros/author=Jk_Rowlings", 100)
  assert type(r) == str


@patch("library.books.urlopen", return_value=StubHTTPResponse())
def test_make_request_should_return_type_string_3(mock_urlopen):
  r = make_request("https://buscarlivros/author=Jk_Rowlings", 100)
  assert type(r) == str

#Use to substitute required parameter
class Dummy:
  pass

def mock_expection_http_error(url, timeout):
  fp = mock_open
  fp.close = Dummy
  raise HTTPError(Dummy(), Dummy(), "messagem de error", Dummy(), fp)

def test_make_request_should_return_excpetion_http_error():
  with patch("library.books.urlopen", mock_expection_http_error):
    with pytest.raises(HTTPError) as exception:
      make_request_no_try_catch("https://buscarlivros/author=Jk_Rowlings", 100)
    assert "messagem de error" in str(exception.value)

#using unittest.mock
@patch("library.books.urlopen")
def test_make_request_should_return_excpetion_http_error_1(mock_urlopen):
  fp = mock_open()
  fp.close = Dummy
  mock_urlopen.side_effect = HTTPError(Dummy(), Dummy(), "messagem de error", Dummy(), fp)
  with pytest.raises(HTTPError) as exception:
    make_request_no_try_catch("https://buscarlivros/author=Jk_Rowlings", 100)
    assert "messagem de error" in str(exception.value)

#using unittest.mock
@patch("library.books.urlopen")
def test_make_request_should_return_excpetion_http_error_2(mock_urlopen):
  fp = mock_open()
  fp.close = Mock()
  mock_urlopen.side_effect = HTTPError(Mock(), Mock(), "messagem de error", Mock(), fp)
  with pytest.raises(HTTPError) as exception:
    make_request_no_try_catch("https://buscarlivros/author=Jk_Rowlings", 100)
    assert "messagem de error" in str(exception.value)


def test_should_execute_request_and_log_msg_http_error(caplog):
  with patch("library.books.urlopen", mock_expection_http_error):
    result = make_request("http:://", 100)
    m = "messagem de error"
    assert len(caplog.records) == 1
    for register in caplog.records:
      assert m in register.message

#unitest
#stub
@patch("library.books.urlopen")
def test_should_execute_request_and_log_msg_http_error_1(stub_urlopen, caplog):
  fp = mock_open()
  fp.close = Mock()
  stub_urlopen.side_effect = HTTPError(Mock(), Mock(), "messagem de error", Mock(), fp)
  make_request("http:://", 100)
  m = "messagem de error"
  assert len(caplog.records) == 1
  for register in caplog.records:
    assert m in register.message


