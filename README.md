# Learning more about Doubles (mock, spy, stub) test for python



This repository is to understand about how mocks works in python and use mocks, stub, spy in python to visualizate the concepts about.
All code here is only for study.

Remember all code her is to study to improve this code.
- You can change urllib to request
- You can use  a better way to write in file system
- I believe that there are some functions that are using a lot of mocks, we could break into more unitary functions so we don't need to use mocks


This codes try to simulate:
- How your code works when you calls external APIs and then don't return an payload.
- How your code works when try to write/read in files system and get a IOError
- How your code works when try to calls externals database and then don't return.


### Attention:

This content was for learning about python mocks.
I believe that if you need to create a lot of mocks to
test a function, it may be too tight and we can try
some refactoring techniques to remove some dependencies and create unit tests


# Aprendendo sobre Mocks em python

Esse repo é para aprender um pouco sobre como mocks, magic mock e as libs de python são implmentadas.
Todo conteúdo aqui é para realizar mocks de chamas externas.

Por exemplo:
- Garantir como seus sistema vai se comportar com chamadas de apis externas, caso elas não respondam
- Garantir como seu sistema vai se comportar quando tentar realizar I/O em disco e falhar a escrita ou leitura.
- Garantir como seus sistema se comporta quando tentar escrever em um banco dados ou ler e o mesmo não estiver respondendo.


### Atenção:

Este conteudo foi para aprender sobre mocks em python.
Acredito que quanto se você precisa criar muitos mocks
para testar uma função talvez ela esteja muito acoplada
e podemos tentar algumas tecnicas de refactoring para
remover algumas depencencias e criar testes unitarios



## Links

https://blog.cleancoder.com/uncle-bob/2014/05/14/TheLittleMocker.html

http://xunitpatterns.com/Test Double Patterns.html

https://docs.python.org/3/library/unittest.mock.html





