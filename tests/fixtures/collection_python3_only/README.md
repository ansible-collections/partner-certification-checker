# local.python3_only_collection

Minimal Python 3-only test collection used to validate the
`sanity-target-python-versions` input. It declares
`requires_ansible: ">=2.16.0"` in `meta/runtime.yml` but its module uses
Python 3 type hints incompatible with Python 2.7, and it carries no
`compile-2.7`/`import-2.7` sanity ignore entries. If the
`sanity-target-python-versions` input stops excluding Python 2.7 from the
`stable-2.16` sanity job, this collection's sanity checks fail.
