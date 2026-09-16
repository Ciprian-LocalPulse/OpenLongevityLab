# Reproducibility

Pin runtime and dependency versions, record source snapshots and transformation parameters, and use deterministic seeds for stochastic analyses. Synthetic fixtures make core grading and gap detection reproducible without network credentials.

## Choose the operation to reproduce

Start with a concrete claim rather than attempting to reproduce the whole platform at once. Examples include constructing an evidence record, replaying a provider fixture, calculating a navigation score, storing a publication revision, or listing persisted records through the API. Identify the expected output and the boundary of the claim. A parser replay and a successful live request establish different properties and should have separate records.

The current repository combines implemented infrastructure, synthetic demonstrations, and proposed methods. Reproducing a fixture response does not reproduce a scientific study. Running the ordinary-least-squares baseline does not validate an aging clock. This guide provides an operational procedure for producing inspectable execution evidence while [the academic protocol](docs/academic/10-reproducibility-protocol.md) explains the methodological distinctions behind it.

## Capture the checkout before execution

Record the exact commit and whether the working tree contains changes. If an experiment depends on uncommitted edits, retain those edits as a patch or a separate commit. Do not identify a modified checkout only by the nearest release tag. A branch name is useful for locating work but can move, so it is not a sufficient identifier for a reproducibility package.

```bash
git rev-parse HEAD
git status --short
git diff --stat
```

Preserve the command outputs with the experiment record. If the repository was obtained from a fork, record the relevant remote and commit without exposing embedded credentials. Do not rewrite existing tags to align them with a later environment or correction. A failed attempt against an older revision is still useful evidence when its scope and limitations are described accurately.

## Prepare an explicit environment

Use an isolated Python environment and record the interpreter version. Install the extras required by the operation: the current API application imports database components, so include database dependencies for API work. Capture resolved dependencies rather than only the allowed version ranges in the project manifest. The same manifest can resolve differently at another time or on another platform.

```bash
python --version
python -m venv .venv
pip install -e ".[dev,api,db]"
python -m pip freeze
```

Activate the new environment before installation using the syntax appropriate to the shell. In PowerShell this normally uses the Scripts directory; a POSIX shell normally uses the bin directory. State which shell was used when command syntax matters. A reader should not have to infer whether a command ran under the intended environment or a globally installed interpreter with additional packages.

Configuration belongs in the record, but secrets do not. Describe which variables were set, which backend was used, and whether live providers were enabled. Replace credential values with placeholders. A public reproduction should permit an authorized operator to supply their own configuration rather than require disclosure of the original operator's ingestion key or database password.

## Run the smallest offline check

Begin with an example that does not depend on external network conditions. The whitepaper contains current constructor and multi-omics examples, and the test suite includes deterministic cases. Execute the relevant example and compare the result with the documented expectation. If the example fails, preserve the error and environment before changing anything; that observation can identify an interface discrepancy or missing prerequisite.

```bash
pytest
ruff check .
```

Report test passes, failures, and skips separately. A skipped PostgreSQL case is not a successful database integration result. Ruff checks a configured set of static rules; it does not establish statistical correctness or scientific interpretation. A test count is meaningful only with the commit and command that produced it, because later changes can alter both the number of tests and their coverage.

## Reproduce the publication storage path separately

Use a disposable PostgreSQL database for migration and repository tests. Verify the target configuration before running commands that write schema or content. The repository uses PostgreSQL-specific operations, so an in-memory substitute does not exercise the same transaction and constraint behavior. The test seed is synthetic and is not a provider-ingestion demonstration.

```bash
alembic upgrade head
pytest -m postgres
```

Record the database version and migration revision, then test the operation relevant to the claim. Repeated retrieval of unchanged content should be distinguished from a new content revision. Concurrent writes, identity collisions, and a failed batch require their own cases. Ingestion currently commits individual publications, so a later failure can leave earlier records persisted. Document that state before retrying rather than assume a complete rollback.

For a recovery claim, restore a backup into an isolated environment and inspect the resulting schema and content. A backup file existing is not evidence of successful restoration. Record what was checked after recovery and what was outside the examination. No general production-recovery guarantee follows from the availability of a migration command.

## Record live retrieval without promising identical results

A live-source check should retain provider identity, query, retrieval time, requested limits, observed identifiers, parser version, and classified errors. Upstream databases evolve, so repeating the request may yield different metadata or a different result set. Explain whether the objective is current connectivity, parser compatibility, or exact replay of a retained response. Those objectives need different artifacts.

If a fixture is retained, document its origin and redistribution basis. A checksum needs a definition of the hashed object: canonicalized article XML and normalized publication JSON are not the same artifact. Do not imply that a full network exchange can be reconstructed when only a normalized record was stored. Unknown source fields should remain unknown in the replay material.

## Control transformations and time-dependent behavior

Preserve preprocessing parameters, feature definitions, record selection, and model state when reproducing an analysis. A random seed controls only randomness actually governed by that seed; it does not pin dependencies, source data, parallel execution, or wall-clock inputs. The current navigation score uses the current UTC date for publication-age weighting, so an otherwise unchanged run can yield a different dated score.

Capture the execution time for that score and state the limitation. A future explicit as-of parameter would improve control, but it must not be documented as already implemented. The same principle applies to normalization: changing a parser or feature transformation can change output without a change in the original study. Preserve those transformation versions separately from the package version.

## Package the evidence and limitations

A useful reproduction bundle contains the question, code identity, environment, input manifest, commands, expected result, actual result, and explanation of deviations. Include only data that can appropriately be shared. Where access is restricted, provide a documented access path and synthetic verification cases without pretending that those cases reproduce the private study's findings.

The documentation audit and Mermaid checker provide additional structural evidence for the written corpus. Their reports do not certify scientific content or rendered visual quality. See [the script guide](scripts/README.md) for exact commands and scope. The final reproduction statement should name the operation successfully repeated and preserve every material limitation, allowing another reader to judge the result without relying on an unqualified reproducible badge.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
