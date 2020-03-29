import pytest
from library import __version__
from library.books import Response, Search, download_book, make_request
from unittest.mock import patch, mock_open, Mock, MagicMock, call

from urllib.error import HTTPError


@pytest.fixture
def resultado_em_duas_paginas():
    return [
        """
        {
            "num_docs": 5,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]
        }
        """,
        """
        {
            "num_docs": 5,
            "docs": [
                {"author": "Kenneth Reitz",
                 "title": "O Guia do Mochileiro Python"
                },
                 {"author": "Wes McKinney",
                 "title": "Python Para Análise de Dados"
                }
            ]
        }
        """,
    ]


@pytest.fixture
def resultado_em_tres_paginas():
    return [
        """
        {
            "num_docs": 8,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]
        }
        """,
        """
        {
            "num_docs": 8,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]
        }
        """,
        """
        {
            "num_docs": 8,
            "docs": [
                {"author": "Kenneth Reitz",
                 "title": "O Guia do Mochileiro Python"
                },
                 {"author": "Wes McKinney",
                 "title": "Python Para Análise de Dados"
                }
            ]
        }
        """,
    ]


@pytest.fixture
def conteudo_de_4_arquivos():
    return [
        """
        {
            "num_docs": 17,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]
        }
        """,
        """
        {
            "num_docs": 17,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]

        }
        """,
        """
        {
            "num_docs": 17,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]
        }
        """,
        """
        {
            "num_docs": 17,
            "docs": [
                {"author": "Kenneth Reitz",
                 "title": "O Guia do Mochileiro Python"
                },
                 {"author": "Wes McKinney",
                 "title": "Python Para Análise de Dados"
                }
            ]
        }
        """,
    ]


@pytest.fixture
def resultado_em_tres_paginas_erro_na_pagina_2():
    return [
        """
        {
            "num_docs": 8,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]
        }
        """,
        None,
        """
        {
            "num_docs": 8,
            "docs": [
                {"author": "Kenneth Reitz",
                 "title": "O Guia do Mochileiro Python"
                },
                 {"author": "Wes McKinney",
                 "title": "Python Para Análise de Dados"
                }
            ]
        }
        """,
    ]


@pytest.fixture
def resultado_em_tres_paginas_erro_na_pagina_1():
    return [
        None,
        """
        {
            "num_docs": 8,
            "docs": [
                {"author": "Luciano Ramalho",
                 "title": "Python Fluente"
                },
                {"author": "Nilo Ney",
                 "title": "Introdução a Programação com Python"
                },
                 {"author": "Allen B. Downey",
                 "title": "Pense em Python"
                }
            ]
        }
        """,
        """
        {
            "num_docs": 8,
            "docs": [
                {"author": "Kenneth Reitz",
                 "title": "O Guia do Mochileiro Python"
                },
                 {"author": "Wes McKinney",
                 "title": "Python Para Análise de Dados"
                }
            ]
        }
        """,
    ]

#Mock (spy and stub)
class MockSearch:
    def __init__(self):
        self.calls = []
        self.search = []

    def Search(self, author=None, title=None, book=None):
        searched = Search(author, title, book)
        self.calls.append((author, title, book))
        self.search.append(searched)
        return searched

    def verifier(self):
        assert len(self.search) == 1
        assert self.calls == [(None, None, "Python")]


@patch("library.books.make_request")
def test_baixar_livros_instancia_Consulta_uma_vez(
    stub_executar_requisicao, resultado_em_duas_paginas
):
    mock_consulta = MockSearch()
    stub_executar_requisicao.side_effect = resultado_em_duas_paginas
    Response.qtd_docs_por_pagina = 3
    arquivo = ["/tmp/arquivo1", "/tmp/arquivo2", "/tmp/arquivo3"]
    with patch("library.books.Search", mock_consulta.Search):
        download_book(arquivo, None, None, "Python")
        mock_consulta.verifier()



@patch("library.books.make_request")
def test_download_book_chama_executar_requisicao_n_vezes(
    mock_executar_requisicao, resultado_em_duas_paginas
):
    mock_executar_requisicao.side_effect = resultado_em_duas_paginas
    Response.qtd_docs_por_pagina = 3
    arquivo = ["/tmp/arquivo1", "/tmp/arquivo2", "/tmp/arquivo3"]
    download_book(arquivo, None, None, "python")
    assert mock_executar_requisicao.call_args_list == [
        call("https://buscarlivros?q=python&page=1", 10),
        call("https://buscarlivros?q=python&page=2", 10),
    ]


@patch("library.books.make_request")
def test_download_book_instancia_Resposta_tres_vezes(
    stub_executar_requisicao, resultado_em_tres_paginas
):
    stub_executar_requisicao.side_effect = resultado_em_tres_paginas
    Response.qtd_docs_por_pagina = 3
    arquivo = ["/tmp/arquivo1", "/tmp/arquivo2", "/tmp/arquivo3"]
    with patch("library.books.Response") as MockResposta:
        MockResposta.side_effect = [
            Response(resultado_em_tres_paginas[0]),
            Response(resultado_em_tres_paginas[1]),
            Response(resultado_em_tres_paginas[2]),
        ]
        download_book(arquivo, None, None, "python")
        assert MockResposta.call_args_list == [
            call(resultado_em_tres_paginas[0]),
            call(resultado_em_tres_paginas[1]),
            call(resultado_em_tres_paginas[2]),
        ]


@patch("library.books.make_request")
def test_download_book_chama_escrever_em_arquivo_tres_vezes(
    stub_executar_requisicao, resultado_em_tres_paginas
):
    stub_executar_requisicao.side_effect = resultado_em_tres_paginas
    Response.qtd_docs_por_pagina = 3
    arquivo = ["/tmp/arquivo1", "/tmp/arquivo2", "/tmp/arquivo3"]
    with patch("library.books.write_file") as mock_escrever:
        mock_escrever.return_value = None
        download_book(arquivo, None, None, "python")
        assert mock_escrever.call_args_list == [
            call(arquivo[0], resultado_em_tres_paginas[0]),
            call(arquivo[1], resultado_em_tres_paginas[1]),
            call(arquivo[2], resultado_em_tres_paginas[2]),
        ]


@patch("library.books.make_request")
def test_download_book_chama_escrever_em_arquivo_para_pagina_1_e_3(
    stub_executar_requisicao, resultado_em_tres_paginas_erro_na_pagina_2
):
    stub_executar_requisicao.side_effect = resultado_em_tres_paginas_erro_na_pagina_2
    Response.qtd_docs_por_pagina = 3
    arquivo = ["/tmp/arquivo1", "/tmp/arquivo2", "/tmp/arquivo3"]
    with patch("library.books.write_file") as mock_escrever:
        mock_escrever.side_effect = [None, None]
        download_book(arquivo, None, None, "python")
        assert mock_escrever.call_args_list == [
            call(arquivo[0], resultado_em_tres_paginas_erro_na_pagina_2[0]),
        ]


@patch("library.books.make_request")
def test_download_book_chama_escrever_em_arquivo_para_pagina_2_e_3(
    stub_executar_requisicao, resultado_em_tres_paginas_erro_na_pagina_1
):
    stub_executar_requisicao.side_effect = resultado_em_tres_paginas_erro_na_pagina_1
    Response.qtd_docs_por_pagina = 3
    arquivo = ["/tmp/arquivo1", "/tmp/arquivo2", "/tmp/arquivo3"]
    with patch("library.books.write_file") as mock_escrever:
        mock_escrever.side_effect = [None, None]
        download_book(arquivo, None, None, "python")
        assert mock_escrever.call_args_list == [
            call(arquivo[1], resultado_em_tres_paginas_erro_na_pagina_1[1]),
            call(arquivo[2], resultado_em_tres_paginas_erro_na_pagina_1[2]),
        ]
