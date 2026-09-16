# Scripts

Maintenance scripts should be deterministic, reviewable, and safe to rerun. Network ingestion scripts must document API terms, rate limits, licensing, and a dry-run mode before they are added.

## Script categories and operating assumptions

Scripts in this directory support maintenance and verification rather than define the scientific API. Their behavior should be evaluated individually. Reading documentation, validating diagram syntax, and seeding a database have different effects and prerequisites. A script being located in a maintenance directory does not make every execution read-only or safe against an arbitrary environment. Inspect its inputs, outputs, and target before running it.

The documentation tools added during the academic audit are read-only with respect to the Markdown corpus. They print reports to standard output, allowing an operator to retain generated JSON separately. The test seed script writes database content and belongs in a disposable test environment. It is not a live-source ingestion command. This distinction should remain visible in automated workflows and in examples copied into a local shell.

## Documentation inventory and prose counting

Run the Python audit from the repository root with the environment used for development. The script uses the Git index to enumerate tracked Markdown files, including root documents, nested research notes, and the pull-request template. It excludes untracked files and non-Markdown machine metadata. New documents must be added to the index before the tracked-file inventory can evaluate them. That scope is intentional and is reported in the generated result.

```bash
python scripts/audit_documentation.py
python scripts/audit_documentation.py --json
```

The default minimum is one thousand prose words. Fenced code and Mermaid source do not contribute to this count. Inline code, image markup, and URL destinations are also removed before words are counted. Ordinary headings and link labels remain part of the narrative text. The resulting count is a documented editorial measure, not a universal linguistic definition of a word or a certification of academic quality.

Each record reports its path, prose count, diagram count, local-link findings, issue labels, and a hash of normalized text. The hash uses the text representation read by Python, including its newline normalization; it should not be described as the original file's byte-for-byte digest. It helps identify which document content was measured without implying that the script has assessed the truth of its claims.

The command returns a nonzero exit status while any tracked document fails the requirements. That behavior is expected during an incomplete expansion. Do not suppress the result or lower the threshold merely to create a green badge. A report can legitimately demonstrate that attribution and local targets pass while many documents remain below the requested length. The backlog is an output of the audit, not a failure to run the tool.

## What the structural audit does not check

The Python audit checks inline Markdown link and image targets and HTML source or hyperlink attributes for local file existence. It does not validate external web availability, reference-style Markdown links, or URL fragments. A link to an existing document can therefore still point to an absent heading. Those limitations are declared in the script and should be considered when interpreting a clean structural result.

The audit detects unclosed fenced blocks and requires Mermaid blocks in numbered academic notes. It does not parse Mermaid syntax. It also cannot decide whether prose is repetitive, a method is statistically appropriate, a citation supports a claim, or a diagram overstates implementation status. Human review and separate execution checks are necessary for those questions. Word count should remain one part of a broader editorial process.

## Mermaid syntax verification

The JavaScript checker parses the Mermaid blocks used by the corpus. Its dependencies can be installed in an isolated tooling directory outside the product environment. The example below uses a sibling directory named documentation-tools. That directory contains generated package installation material and should not be added to the application merely to satisfy this check.

```bash
npm install --prefix ../documentation-tools --ignore-scripts --no-audit --no-fund mermaid@11.17.2 jsdom@26.1.0
node scripts/check_mermaid.mjs . ../documentation-tools
```

The first argument selects the repository and the second selects the installed tooling directory. The checker uses a DOM environment for Mermaid parsing, enumerates tracked Markdown, and reports each diagram's status. It supports the column-zero triple-backtick Mermaid fences currently used in this corpus. If documentation adopts another fence convention, update the checker and its reported scope before relying on its diagram count.

Successful parsing establishes syntax acceptance under the recorded Mermaid version. It does not establish a readable visual layout, a correct scientific argument, or correspondence between the diagram and executable code. A separate rendered review is needed for overlapping labels, ambiguous arrows, and poor contrast. The audit report must not relabel syntax validation as complete visual verification.

## Synthetic database seeding

The existing seed script inserts synthetic publication material for tests. It may obtain its connection from the test database variable or fall back to the general database variable. Verify the resolved environment before running it and use a database intended to be disposable. A seed inserted directly into storage does not demonstrate that a real provider was contacted, that a parser succeeded, or that publication revision behavior was exercised through the repository interface.

The current application's publication-origin flag is not sufficient to identify every such seeded record correctly. This limitation is documented in the whitepaper and needs an implementation fix with a regression test. Until then, operators must retain the origin of test data through their environment and workflow records rather than infer authenticity from the serialized flag alone. Do not use the seed as a shortcut for populating a public scientific demonstration with apparently genuine records.

## Maintaining verification scripts

Changes to a verifier can change the meaning of a reported pass. When modifying counting rules, file discovery, link handling, or diagram parsing, explain the new scope and compare representative cases. A useful verifier should fail transparently when its prerequisites are unavailable. It should not silently skip malformed input and then report the remaining cases as a complete audit.

Keep generated reports separate from hand-authored narrative. Reports can be regenerated from the documented command, while prose should explain the interpretation and limitations of the result. Record the software revision and tool versions alongside consequential findings. A report produced from a modified working tree should not be attributed to an unchanged release tag. This discipline makes maintenance tooling useful evidence without asking it to certify properties it cannot measure.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
