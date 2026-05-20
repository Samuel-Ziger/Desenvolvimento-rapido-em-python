# Sistema de Cadastro de Alunos

Trabalho de Desenvolvimento Rápido em Python — Estácio.

## Tecnologias

- Python 3.10+
- Tkinter (interface gráfica)
- SQLite (banco de dados)

## Funcionalidades

Sistema CRUD completo para três entidades:

- **Manter Aluno** — matrícula, nome, data de nascimento
- **Manter Disciplina** — nome, turno, sala, professor
- **Manter Nota** — vínculo aluno × disciplina × valor da nota

Todas as funcionalidades possuem **Listar, Incluir, Alterar e Excluir**.

### Extras implementados

- Validação de campos (matrícula, datas, faixa de notas, turnos)
- Busca/filtro em tempo real nas listagens
- Relatório de boletim por aluno (com média e situação)
- Exportação automática de todos os dados nos formatos **JSON, CSV e TXT** (botão na tela principal — gera arquivos na pasta `exports/`)

## Estrutura do projeto

```
sistema_cadastro_alunos/
├── main.py                       # Entry point
├── database/
│   └── db.py                     # Conexão SQLite + criação das tabelas
├── models/                       # Dataclasses
│   ├── aluno.py
│   ├── disciplina.py
│   └── nota.py
├── controllers/                  # Lógica de CRUD
│   ├── aluno_controller.py
│   ├── disciplina_controller.py
│   └── nota_controller.py
├── views/                        # Telas Tkinter
│   ├── main_window.py
│   ├── aluno_window.py
│   ├── disciplina_window.py
│   ├── nota_window.py
│   └── relatorio_window.py
├── utils/
│   ├── validators.py             # Validações de campos
│   └── exporters.py              # Exportação JSON / CSV / TXT
├── exports/                      # Gerada em runtime ao exportar
└── sistema_alunos.db             # Banco SQLite (criado em runtime)
```

## Modelo de Dados

```
ALUNO                  DISCIPLINA              NOTA
─────────              ──────────              ────────────────
matricula (PK)         id (PK)                 valor
nome                   nome                    matricula     (FK aluno)
dt_nascimento          turno                   disciplina_id (FK disciplina)
                       sala                    PK composta (matricula, disciplina_id)
                       professor
```

Chaves estrangeiras com `ON DELETE CASCADE`: ao excluir aluno ou disciplina,
as notas vinculadas são automaticamente removidas.

## Como executar

```bash
cd sistema_cadastro_alunos
python main.py
```

A primeira execução cria automaticamente o arquivo `sistema_alunos.db`.

## Fluxo de uso sugerido para apresentação

1. Cadastrar **disciplinas** primeiro (gera os IDs)
2. Cadastrar **alunos** (com suas matrículas)
3. Lançar **notas** combinando aluno + disciplina
4. Abrir **Relatório / Boletim** para visualizar a média de um aluno
5. Clicar em **Exportar Todos os Dados** para gerar os arquivos JSON/CSV/TXT

## Requisitos atendidos da especificação

- [x] Manter Aluno (CRUD completo)
- [x] Manter Disciplina (CRUD completo)
- [x] Manter Nota (CRUD completo)
- [x] Linguagem Python
- [x] Banco de Dados SQLite
- [x] Interface gráfica Tkinter
- [x] Persistência em arquivo (JSON, CSV e TXT)
- [x] Modelo de dados conforme diagrama da especificação
