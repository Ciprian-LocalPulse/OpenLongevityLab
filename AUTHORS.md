# Author

**CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent**

Independent Romanian researcher; founder and principal author of OpenLongevity.

## Purpose of this authorship record

This document identifies responsibility for the OpenLongevity project and explains how project authorship should be represented in documentation, software distributions, citations, and derivative work. It is an attribution record rather than a curriculum vitae. No academic degree, institutional appointment, research employment, publication history, or professional certification is asserted here beyond the role and independent status supplied by the project author. Readers should evaluate the project through its inspectable methods and implementation rather than infer credentials from its presentation.

The author's name should retain its Romanian diacritics: Ciprian Ștefan Pleșca. Uppercase presentation may be used in a footer or author heading without changing the underlying name. The Romanian designation is cercetător român independent; the English rendering is independent Romanian researcher. These descriptions refer to the author's independent research activity. They do not identify a university, government laboratory, employer, or external organization as responsible for the repository.

The portrait below is the image supplied by the author for the project author section. Its inclusion associates a person with the repository's stated project roles. It should not be repurposed to imply an endorsement of external products, clinical advice, institutional partnerships, or scientific claims beyond the project. A source photograph is an attribution asset, not evidence that a particular feature has been independently evaluated.

## Distinguishing project authorship from source authorship

OpenLongevity organizes research metadata and develops computational infrastructure. Its project author is not thereby the author of the publications retrieved through provider interfaces. A publication's original authors, journal, identifier, and applicable terms should remain attributable to that publication. Similarly, a third-party software dependency remains the work of its maintainers under its own license. A consistent project footer should coexist with those credits rather than replace them.

This distinction matters when information moves between formats. A screenshot may show the OpenLongevity name prominently while displaying a study title beneath it. An exported record may include project provenance and upstream authors in different fields. A research note may explain an external statistical method. In each case, the reader should be able to tell who authored the infrastructure, who produced the original evidence, and who performed any subsequent interpretation. Combining those responsibilities into a single author field would obscure the chain of contribution.

Project documentation should also distinguish a method's origin from an implementation of that method. Implementing a familiar estimator does not transfer authorship of the estimator's mathematical foundations to this project. Conversely, citing a methodological reference does not show that the local implementation is correct. Credit and verification answer different questions, and both should remain visible in a scholarly software record.

## Responsibility attached to the listed roles

Founder identifies responsibility for initiating the project and defining its broad direction. Project Creator identifies authorship of the project concept and repository identity. Lead Maintainer identifies responsibility for reviewing changes, managing integration, and maintaining coherent interfaces. Principal Author identifies responsibility for the project's own scientific and technical narrative. These roles can overlap in an independent project while still requiring distinct forms of work and accountability.

A maintainer deciding whether to merge a change should consider correctness, reproducibility, compatibility, and the clarity of its limitations. A documentation author should check whether examples execute and whether the prose accurately separates implemented behavior from future design. A researcher interpreting an output should examine data provenance and methodological assumptions. Having one person hold multiple project roles does not remove the need to make these different judgments explicit.

The roles listed here do not mean that every future contribution must be attributed exclusively to the founder. Contributions should receive credit proportionate to their actual content. Git history records who supplied changes, but commit authorship alone may not capture conceptual design, data annotation, methodological review, or error discovery. Where those contributions are material, the relevant document or release record should describe them plainly without inventing participation or honorary authorship.

## A contribution attribution protocol

For a substantive contribution, record what changed, why it matters, and which artifacts demonstrate the work. A parser contribution might include implementation, representative fixtures, and analysis of unsupported source patterns. A research-note contribution might include problem formulation, derivation, review of assumptions, and an executable example. An audit contribution might identify a reproducible defect or correct an unsupported maturity claim. Each should be described according to what was actually delivered.

Before adding another person's name, verify the spelling and the intended attribution. Publicly visible discussion does not automatically make someone a coauthor. A passing comment, issue report, detailed technical review, and jointly written paper are different contributions. If contribution roles change over time, update the relevant record while preserving the historical explanation. Avoid claiming that an unnamed scientific committee, external reviewer, or institutional partner has approved the work.

Automated assistance should be described as a tool-supported activity when disclosure is relevant to understanding the artifact. A model does not assume the accountability of a human author. The person submitting text or code remains responsible for checking citations, licenses, scientific assertions, and test results. Generated references must be verified against their actual sources, and generated code must be evaluated through the same review process as other contributions.

## Citation and reproducible identification

Use the repository's [citation metadata](CITATION.cff) as a starting point for a software citation, then identify the exact commit or immutable release actually used. If the citation file's version differs from a working checkout, do not silently cite that version as though it describes the checkout. Record the commit explicitly. A branch name is convenient for navigation but can move; it is not an immutable identifier for a scientific result.

Software citation and data citation should be separate. A report produced with OpenLongevity may need to cite the software, the original publications, the metadata provider, and any external reference implementation used for verification. Retrieval dates and parser versions are part of computational provenance rather than substitutes for scholarly attribution. A reader should be able to locate the source and reconstruct the transformation without guessing which party supplied each element.

The project should not invent a digital object identifier, archived release, peer-reviewed publication, or institutional repository deposit. If an archival record becomes available, its identifier should be verified before inclusion. Until then, the public repository and an exact commit provide a clear account of what is being referenced, with the limitations of that distribution mechanism stated honestly.

## Contact, correction, and independent identity

Project discussion and reproducible correction reports can use the [GitHub repository](https://github.com/Ciprian-LocalPulse/OpenLongevityLab). Reports should identify the affected document or code path and explain the observed issue. Sensitive security details should follow [the security policy](SECURITY.md) rather than be included in a public reproduction. No additional personal contact information is created by this authorship document.

The author attribution should accompany project documents in a restrained footer and appear prominently in author-focused materials. It should not crowd out the method, source citation, or limitation statement that a researcher needs to evaluate a result. The value of naming an author lies in accountable responsibility: readers know whose project they are examining and where corrections should be directed. It does not turn a draft into validated scholarship or establish an affiliation that has not been claimed and verified.

<img src="docs/assets/author.jpeg" alt="Portrait of Ciprian Ștefan Pleșca" width="240">

## Ciprian Ștefan Pleșca

- Founder
- Project Creator
- Lead Maintainer
- Principal Author

OpenLongevity — Open-source computational infrastructure for aging and longevity research.
