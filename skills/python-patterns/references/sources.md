# Python source basis

This package is a Rundesk synthesis of primary Python documentation and established maintainer style
guides. The operational guidance is contained in the local Markdown references; use this file to
audit or update a claim. Where sources permit multiple conventions, the skill tells agents to follow
the repository instead of presenting one organization's choice as Python law.

## Language-wide style and contracts

- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/): imports, module-level
  order, comments, naming, inheritance APIs, public/internal interfaces, annotations, and the rule
  that project consistency can outweigh a general recommendation.
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/): docstring placement,
  one-line and multiline form, imperative summaries, and caller-visible function, class, module,
  package, and script documentation.
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/): annotations as optional type metadata
  and their relationship to runtime behavior.
- [PEP 604 — Union Types](https://peps.python.org/pep-0604/): the Python 3.10 version floor for
  `X | Y` union syntax.
- [PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/): readability, explicit behavior,
  simplicity, flat structure, and namespaces as guiding—not mechanically enforceable—principles.

## Modules, packages, and entry points

- [Python tutorial — Modules and Packages](https://docs.python.org/3/tutorial/modules.html): import
  execution, module namespaces, package structure, `__init__.py`, `__all__`, wildcard imports,
  absolute and relative imports, and directly executed modules.
- [Python `__main__` documentation](https://docs.python.org/3/library/__main__.html): minimal entry
  blocks, importable `main()` behavior, exit values, and package `__main__.py`.
- [Python Packaging User Guide — `src` layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/): the isolation, installation, and import-path tradeoffs of each project layout.

## Established project conventions

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html): explicit dos and
  don'ts for imports, mutable global state, nesting, defaults, properties, docstrings, comments,
  TODOs, naming, import-safe entry points, focused functions, concurrency, and annotations. This is
  a published Google convention, not a universal Python mandate.
- [Python Developer's Guide — Documentation style](https://devguide.python.org/documentation/style-guide/): precise reference prose, simple language, affirmative guidance, and choosing tutorial,
  how-to, reference, or explanation according to the reader's need.

## Concurrency and performance

- [Python concurrency overview](https://docs.python.org/3/library/concurrency.html): selecting
  concurrent tools from CPU-bound versus I/O-bound work and execution style.
- [`asyncio` coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html): task
  ownership, weak task references, cancellation cleanup, timeouts, and structured concurrency.
- [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html): executor
  ownership, shutdown, thread pools, process pools, futures, and deadlock cautions.
- [`multiprocessing` programming guidelines](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines): safe imports, process start methods, resource passing, queues, joining, and avoiding shared state.
- [Python profiling tools](https://docs.python.org/3/library/profile.html): measuring execution before
  optimizing and choosing deterministic or statistical profiling tools.
- [Python data model — `__slots__`](https://docs.python.org/3/reference/datamodel.html#slots): memory,
  attribute, inheritance, weak-reference, and default-value consequences.
