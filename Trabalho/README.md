# Sistema de Cadastro de Alunos

Aplicação desktop em Python com interface gráfica (`tkinter`) para gerenciamento de:

- alunos;
- disciplinas;
- notas.

Os dados são persistidos em banco SQLite e também exportados em JSON para backup.

## Funcionalidades

- Cadastro de alunos (incluir, alterar, excluir e listar).
- Cadastro de disciplinas (incluir, alterar, excluir e listar).
- Lançamento de notas por aluno/disciplina (incluir, alterar, excluir e listar).
- Validações básicas de formulário:
  - data de nascimento no formato `DD/MM/AAAA`;
  - nota entre `0` e `10`.
- Criação automática do banco de dados ao iniciar.
- Exportação automática para JSON após atualizações.

## Estrutura do projeto

- `sistema_cadastro_alunos.py`: arquivo principal da aplicação.
- `escola.db`: banco SQLite (criado automaticamente na primeira execução).
- `escola_backup.json`: backup JSON dos dados (gerado automaticamente).

## Requisitos

- Python `3.8+` (recomendado).
- Biblioteca `tkinter` disponível no ambiente.

> Observação: `sqlite3`, `json` e `datetime` já fazem parte da biblioteca padrão do Python.

## Como executar

No diretório do projeto, execute:

```bash
python sistema_cadastro_alunos.py
```

Se o comando acima não funcionar, tente:

```bash
python3 sistema_cadastro_alunos.py
```

## Instalação do tkinter (se necessário)

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3-tk
```

### Fedora

```bash
sudo dnf install python3-tkinter
```

### Windows/macOS

Na maioria dos casos, o `tkinter` já vem com a instalação oficial do Python.  
Se não estiver disponível, reinstale o Python pela versão oficial e habilite os componentes Tcl/Tk.

## Banco de dados

As tabelas criadas automaticamente são:

- `ALUNO`
- `DISCIPLINA`
- `NOTA`

Relacionamentos:

- `NOTA.MATRICULA` referencia `ALUNO.MATRICULA`;
- `NOTA.DISCIPLINA_ID` referencia `DISCIPLINA.ID`.

## Observações

- O arquivo `escola.db` fica no mesmo diretório do script.
- O backup `escola_backup.json` é atualizado durante os `refresh` das abas.
- Para começar do zero, remova `escola.db` e execute o sistema novamente.
