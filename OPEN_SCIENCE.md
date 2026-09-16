# Open science

OpenLongevity favors open methods, versioned data contracts, source provenance, and community review. Public scientific APIs should be used according to their terms and attribution requirements. Reproducible transformations and correction histories are part of the research record.

## Meaning of openness in this project

OpenLongevity treats openness as the ability to inspect methods, identify sources, understand decisions, and challenge results. Publishing source code is one part of that commitment, but it does not automatically make a scientific claim reproducible or a dataset reusable. A reader also needs the relevant inputs, transformation versions, assumptions, and interpretation boundaries. This document explains the practices the project seeks to implement and how their completion should be evaluated.

The [UNESCO Recommendation on Open Science](https://www.unesco.org/en/legal-affairs/recommendation-open-science) describes a broad approach encompassing scientific knowledge, infrastructures, communication, and participation. It provides context for the project's open-science objectives. Citing that recommendation does not establish UNESCO endorsement or compliance certification. OpenLongevity must demonstrate its own practices through concrete artifacts and accessible explanations.

The project is authored by Ciprian Ștefan Pleșca, an independent Romanian researcher. Independent status makes clear attribution and inspectable work especially important. It does not justify claiming an institutional partnership that has not been established. The project should invite examination of its methods while remaining precise about who produced, reviewed, and maintains each artifact.

## Open methods before persuasive presentation

A method should be explained at the level needed to understand its inputs, transformations, outputs, and failure cases. For a navigation score, that means publishing the actual arithmetic and explaining why its constants are heuristic. For a parser, it means describing supported source patterns and known losses. For a model, it means identifying the target, preprocessing, evaluation design, and limits of interpretation.

The current repository contains experimental utilities and synthetic demonstrations alongside a real publication-persistence path. Open presentation should preserve those distinctions. An attractive interface or a long academic note must not conceal the fact that a proposed review workflow or external benchmark has not been implemented. A public limitation is useful information that helps others contribute and prevents an infrastructure prototype from being mistaken for validated science.

Diagrams are valuable when they clarify responsibilities and data movement. They become misleading when every proposed component is drawn as though it already operates. The project should label future connections and provide acceptance criteria. Likewise, an executable example should use the current interface, while pseudocode should be identified as such. Openness includes making it easy to discover what cannot yet be reproduced.

## Reusable data without indiscriminate disclosure

Data sharing requires a description of what is being shared and under which conditions it can be reused. Public metadata, restricted source text, synthetic fixtures, and participant measurements are different categories. A software license does not automatically extend to all data obtained by the software. The project should preserve source-specific attribution and rights information and should not replace unknown terms with an assumption of unrestricted reuse.

Synthetic fixtures are useful open artifacts because they can exercise software behavior without representing real participants or publications. Their artificial origin must remain explicit. A plausible identifier, realistic title, or provider-shaped envelope should not make a fixture appear genuine. The current publication-origin serialization limitation is documented in the whitepaper and needs an implementation correction before the flag can serve as a reliable authenticity control.

Restricted data can still support transparent methods through carefully designed access procedures, data dictionaries, and synthetic verification examples. Those examples do not substitute for independent assessment of the real analysis, but they help others inspect the computational interface. The project should explain what remains unavailable and why rather than describe an inaccessible study as fully reproducible merely because its code is public.

## Findability and durable identification

An artifact should have a clear title, author attribution, purpose, version, and relationship to the rest of the repository. A research note should link to the implementation it describes. An exported record should retain provider and source identifiers. A release should identify an immutable commit or tag. These practices make it easier to discover the relevant material and avoid confusing a moving development branch with the version used in a report.

The [FAIR principles](https://www.gofair.foundation/fair-principles) provide a reference for findability, accessibility, interoperability, and reuse. They are useful questions to ask of a data product, not a badge automatically earned by hosting files on GitHub. OpenLongevity should describe the identifiers, access conditions, metadata, and reuse information actually supplied for each artifact rather than make an unsupported blanket FAIR-compliant claim.

Durability also requires correction discipline. If a public document contains an error, preserve enough history to identify the affected version and practical consequence. Do not move an existing release tag to hide the earlier state. A corrected method may require a new output or release; a corrected claim may require a visible explanation. The record of change is part of the scientific communication.

## Participation and accessible explanation

Open participation requires that contributors can understand how to report a problem, propose a change, and interpret the review process. The [contribution guide](CONTRIBUTING.md) explains the local workflow, while [governance](GOVERNANCE.md) identifies current responsibility. The project should avoid implying a large committee or formal peer-review process when decisions are presently maintainer-led. Clear scope is more useful than ceremonial structures unsupported by actual participation.

Technical documentation should be precise without requiring readers to guess the meaning of project-specific terminology. Define evidence grades, confidence fields, fixtures, provenance, and review states where they affect interpretation. The project can maintain an English technical corpus while preserving the author's Romanian name and designation accurately. Translations should retain scientific qualifiers rather than simplify away uncertainty or inferential boundaries.

Feedback from different kinds of users can reveal problems missed by code inspection. A developer may identify a transaction issue, a researcher may identify an inappropriate comparison, and a reader may misunderstand an origin label. Record the problem and evidence without treating one perspective as a substitute for all others. Public discussion should support criticism of claims while remaining respectful toward participants.

## Measuring progress without invented impact

Progress should be reported through observable changes: corrected examples, documented source boundaries, replayable fixtures, resolved defects, and completed evaluation artifacts. Repository activity and document length can describe effort but do not establish scientific impact. Do not invent users, partnerships, discoveries, or clinical benefits to make the project appear mature. A transparent account of unfinished work can be more valuable to collaborators than an unsupported success narrative.

The documentation audit supplies one measurable editorial indicator, including the number of files still below the requested prose threshold. It does not certify academic quality. Tests and Mermaid parsing supply other limited indicators. The final open-science objective is that another person can determine what was done, inspect why it was done, reproduce an appropriate part of it, and challenge its interpretation using evidence that the project has made available responsibly.

---

**Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.**
