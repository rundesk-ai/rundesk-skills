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

## Documented traps and the tools that encode them

A lint rule exists because enough people hit the trap. These catalogs are evidence of which mistakes
are common, not merely style opinions.

- [Python Programming FAQ](https://docs.python.org/3/faq/programming.html): mutable default
  arguments, late-binding closures, assignment never copying, `is` versus `==`, local-versus-global
  scope, augmented assignment on tuple members, quadratic string concatenation, and circular imports.
- [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear): the `B0xx` catalog of real Python traps —
  mutable and computed defaults, `finally` swallowing exceptions, `lru_cache` on methods, late
  binding in loops, ABCs missing `@abstractmethod`, `assertRaises(Exception)`, multi-character
  `.strip()`, and `groupby` reuse.
- [Ruff rules](https://docs.astral.sh/ruff/rules/): the family index. `B` (bugbear), `S` (bandit),
  `DTZ` (naive datetimes), `LOG` and `G` (logging), `ASYNC` (blocking calls in coroutines), `PTH`
  (pathlib), `TRY` (exception handling), `SIM`, `PERF`, `TC`, `ANN`.
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html): mutable defaults raising,
  field ordering under inheritance, the `eq`/`frozen`/`__hash__` interaction, `slots` constraints,
  `replace()` with `init=False`, and `__post_init__` versus base-class `__init__`.
- [Deprecations index](https://docs.python.org/3/deprecations/index.html) and
  [What's new in Python 3.13](https://docs.python.org/3/whatsnew/3.13.html): the removal schedule,
  including `datetime.utcnow()` in 3.15, the asyncio policy API in 3.16, and the PEP 594 modules
  already removed in 3.13.

## Security

- [Ruff `flake8-bandit` (S) rules](https://docs.astral.sh/ruff/rules/#flake8-bandit-s) and
  [Bandit](https://bandit.readthedocs.io/): the vulnerability catalog — shell injection, `eval`,
  pickle, unsafe YAML, weak hashes, non-cryptographic randomness, hardcoded credentials, insecure
  temporary files, disabled certificate verification, XML attacks, and `assert` used for enforcement.
- [`subprocess` security considerations](https://docs.python.org/3/library/subprocess.html#security-considerations):
  the `shell=True` injection warning and the argument-list form that avoids it.
- [`pickle`](https://docs.python.org/3/library/pickle.html), [`secrets`](https://docs.python.org/3/library/secrets.html),
  [`hashlib`](https://docs.python.org/3/library/hashlib.html), [`tempfile`](https://docs.python.org/3/library/tempfile.html),
  and [`tarfile` extraction filters](https://docs.python.org/3/library/tarfile.html#extraction-filters).

## Typing

- [`typing`](https://docs.python.org/3/library/typing.html): deprecated aliases and their version
  floors, `Protocol` and the documented limits of `@runtime_checkable`, `TypedDict`, `Self`,
  `Literal`, `Final`, `NewType`, and the note that the runtime does not enforce annotations.
- [Typing best practices](https://typing.python.org/en/latest/reference/best_practices.html) and
  [mypy documentation](https://mypy.readthedocs.io/): `--strict` as a goal, incremental adoption,
  unannotated function bodies going unchecked, `Any` disabling checking, and duck-typed parameters.
- [PEP 544 — Protocols](https://peps.python.org/pep-0544/),
  [PEP 649 — Deferred annotation evaluation](https://peps.python.org/pep-0649/),
  [PEP 695 — Type parameter syntax](https://peps.python.org/pep-0695/).

## Practitioner sources

Maintainer writing, cited where the documentation states a mechanism but not a judgement.

- [Facts and myths about Python names and values](https://nedbatchelder.com/text/names.html) —
  **Ned Batchelder**. The canonical model of names, values, and the "mutable presto-chango."
- [hasattr() — a dangerous misnomer](https://hynek.me/articles/hasattr/),
  [Please fix your decorators](https://hynek.me/articles/decorators/), and
  [Subclassing in Python redux](https://hynek.me/articles/python-subclassing-redux/) —
  **Hynek Schlawack**, author of `attrs` and `structlog`: why `hasattr` masks errors, why
  `functools.wraps` does not preserve a signature, and the composition-over-subclassing argument
  behind decorator-based data classes.

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
