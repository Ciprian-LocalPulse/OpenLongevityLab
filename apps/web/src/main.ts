type EvidenceItem = {
  identifier: string;
  title: string;
  study_type: string;
  species: string;
  endpoint: string;
  source: string;
  confidence: number;
  score: number;
  level: string;
  synthetic: boolean;
  review_status: string;
  reviewed_by?: string | null;
  reviewed_at?: string | null;
  review_notes?: string | null;
};

type EvidenceSummary = {
  records: number;
  active_records: number;
  mean_confidence: number;
  mean_navigation_score?: number;
  disclaimer: string;
};

type EvidencePayload = {
  items: EvidenceItem[];
  mode: string;
  summary: EvidenceSummary;
  disclaimer: string;
};

type PublicationItem = {
  identifier: string;
  title: string;
  journal?: string | null;
  publication_date?: string | null;
  origin: "unknown" | "manual" | "provider" | "synthetic";
  synthetic: boolean | null;
  retraction_status: string;
  revision: number;
  provenance: {
    source_provider: string;
    source_identifier: string;
    source_url: string;
    retrieved_at: string;
    parser_version: string;
  };
};

type PublicationPayload = {
  items: PublicationItem[];
  total: number;
  mode: string;
  disclaimer: string;
};

type GraphPayload = {
  mode: string;
  nodes: string[];
  edges: Array<{ source: string; target: string; relation: string }>;
  disclaimer: string;
};

type HealthPayload = {
  status: string;
  version: string;
  database: string;
  provider_status: string;
  disclaimer: string;
};

const appRoot = document.querySelector<HTMLDivElement>("#app");
if (!appRoot) throw new Error("Dashboard root is missing");
const root = appRoot;

const state = {
  topic: "cellular senescence",
};

renderShell();
void updateHealth();
void inspectEvidence();

function renderShell(): void {
  root.replaceChildren(
    element("header", { className: "hero" }, [
      element("p", { className: "eyebrow" }, ["Open science · research infrastructure · v0.3.0"]),
      element("h1", {}, ["OpenLongevity"]),
      element("p", { className: "lede" }, [
        "Evidence mapping for biological aging research with source labels, fixture boundaries, and review state visible at the point of use.",
      ]),
      element("nav", { className: "toolbar", ariaLabel: "Primary dashboard views" }, [
        actionButton("Evidence", "evidence", inspectEvidence),
        actionButton("Knowledge Graph", "graph", inspectGraph),
        actionButton("Sources", "sources", inspectSources),
      ]),
    ]),
    element("section", { className: "query-panel" }, [
      element("label", { htmlFor: "topic" }, ["Explore a topic"]),
      element("div", { className: "query-row" }, [
        input("topic", state.topic),
        actionButton("Inspect", "inspect", inspectEvidence),
      ]),
      element("p", { className: "status", id: "status" }, ["API status: checking..."]),
    ]),
    element("section", { id: "result", className: "result", ariaLive: "polite" }, [
      element("p", {}, ["Loading evidence boundary..."]),
    ]),
    element("footer", { className: "site-footer" }, [
      element("div", {}, [
        element("strong", {}, ["OpenLongevity"]),
        element("span", {}, ["Open science for a healthier tomorrow"]),
      ]),
      element("div", {}, [
        element("strong", {}, ["CIPRIAN ȘTEFAN PLEȘCA"]),
        element("span", {}, ["Autor · cercetător român independent · maintainer"]),
      ]),
      element("div", { className: "footer-links" }, [
        link("GitHub", "https://github.com/Ciprian-LocalPulse/OpenLongevityLab"),
        link("Whitepaper", "/WHITEPAPER.md"),
        link("Academic manifesto", "/ACADEMIC_MANIFESTO.md"),
      ]),
      element("small", {}, ["Research use only · Not medical advice · synthetic fixtures stay labeled"]),
    ]),
  );

  document.querySelector<HTMLInputElement>("#topic")?.addEventListener("input", (event) => {
    state.topic = (event.target as HTMLInputElement).value;
  });
}

async function inspectEvidence(): Promise<void> {
  const result = resultRegion();
  result.replaceChildren(element("p", {}, ["Loading evidence and publication context..."]));
  const topic = state.topic.trim();
  if (!topic) {
    result.replaceChildren(element("p", { className: "notice warn" }, ["Enter a topic first."]));
    return;
  }

  const evidence = await fetchJson<EvidencePayload>(
    `/api/v1/evidence?topic=${encodeURIComponent(topic)}`,
  );
  if (!evidence.ok) {
    result.replaceChildren(offlineNotice("The evidence endpoint is unavailable."));
    return;
  }

  const publication = await fetchJson<PublicationPayload>(
    `/api/v1/search?query=${encodeURIComponent(topic)}&page=1&page_size=10`,
  );

  const sections: Node[] = [
    element("div", { className: "section-heading" }, [
      element("div", {}, [
        element("p", { className: "eyebrow" }, ["Evidence boundary"]),
        element("h2", {}, [`${evidence.data.summary.active_records} active fixture record(s)`]),
      ]),
      originLegend(),
    ]),
    summaryGrid(evidence.data.summary, evidence.data.mode),
    evidenceList(evidence.data.items),
  ];

  if (publication.ok) {
    sections.push(publicationList(publication.data));
  } else {
    sections.push(element("article", { className: "notice" }, [
      element("strong", {}, ["Persisted publications are not available"]),
      element("p", {}, [
        "The local API can still show fixture evidence, but publication search needs a configured PostgreSQL repository.",
      ]),
    ]));
  }

  result.replaceChildren(...sections);
}

async function inspectGraph(): Promise<void> {
  const result = resultRegion();
  result.replaceChildren(element("p", {}, ["Loading graph demonstration..."]));
  const graph = await fetchJson<GraphPayload>("/api/v1/graph");
  if (!graph.ok) {
    result.replaceChildren(offlineNotice("The graph endpoint is unavailable."));
    return;
  }
  result.replaceChildren(
    element("div", { className: "section-heading" }, [
      element("div", {}, [
        element("p", { className: "eyebrow" }, ["Knowledge graph"]),
        element("h2", {}, [`${graph.data.nodes.length} nodes · ${graph.data.edges.length} edges`]),
      ]),
      badge(graph.data.mode, "neutral"),
    ]),
    element("ol", { className: "edge-list" }, graph.data.edges.map((edge) => element("li", {}, [
      element("strong", {}, [edge.source]),
      element("span", {}, [edge.relation]),
      element("strong", {}, [edge.target]),
    ]))),
    element("p", { className: "fineprint" }, [graph.data.disclaimer]),
  );
}

function inspectSources(): void {
  resultRegion().replaceChildren(
    element("div", { className: "section-heading" }, [
      element("div", {}, [
        element("p", { className: "eyebrow" }, ["Connected sources"]),
        element("h2", {}, ["Read-only provenance map"]),
      ]),
    ]),
    element("div", { className: "source-grid" }, [
      sourceCard("PubMed", "Implemented ingestion path can mark persisted records as provider-origin."),
      sourceCard("Europe PMC", "Adapter shape exists; persisted provider-origin classification is not yet wired."),
      sourceCard("OpenAlex", "Read-only metadata adapter; use origin labels conservatively."),
      sourceCard("Crossref", "Bibliographic metadata path; not a scientific validation service."),
      sourceCard("ClinicalTrials.gov", "Registry adapter boundary; no mutation of upstream records."),
    ]),
  );
}

async function updateHealth(): Promise<void> {
  const health = await fetchJson<HealthPayload>("/api/v1/health");
  const status = document.querySelector<HTMLParagraphElement>("#status");
  if (!status) return;
  if (health.ok) {
    status.textContent = `API status: ${health.data.status} · database: ${health.data.database} · provider: ${health.data.provider_status}`;
  } else {
    status.textContent = "API status: offline · run the FastAPI service locally";
  }
}

function summaryGrid(summary: EvidenceSummary, mode: string): HTMLElement {
  return element("div", { className: "metric-grid" }, [
    metric("Mode", mode),
    metric("Records", String(summary.records)),
    metric("Active", String(summary.active_records)),
    metric("Mean confidence", formatNumber(summary.mean_confidence)),
    metric("Navigation score", summary.mean_navigation_score == null ? "n/a" : formatNumber(summary.mean_navigation_score)),
  ]);
}

function evidenceList(items: EvidenceItem[]): HTMLElement {
  if (!items.length) {
    return element("article", { className: "notice" }, [
      element("strong", {}, ["No matching fixture evidence"]),
      element("p", {}, ["Try a topic such as cellular senescence."]),
    ]);
  }
  return element("div", { className: "cards" }, items.map((item) => element("article", { className: "record-card" }, [
    element("div", { className: "card-top" }, [
      badge(item.synthetic ? "synthetic fixture" : "non-synthetic", item.synthetic ? "warn" : "ok"),
      badge(item.review_status, item.review_status === "unreviewed" ? "neutral" : "ok"),
      badge(`Level ${item.level}`, "neutral"),
    ]),
    element("h3", {}, [item.title]),
    element("p", {}, [`${item.study_type} · ${item.species} · ${item.endpoint}`]),
    element("dl", { className: "record-meta" }, [
      meta("Identifier", item.identifier),
      meta("Source", item.source),
      meta("Confidence", formatNumber(item.confidence)),
      meta("Navigation score", formatNumber(item.score)),
    ]),
    item.reviewed_by ? element("p", { className: "fineprint" }, [
      `Reviewed by ${item.reviewed_by} at ${item.reviewed_at ?? "unknown time"}. ${item.review_notes ?? ""}`,
    ]) : element("p", { className: "fineprint" }, [
      "Not human verified. Fixture records remain excluded from citation-eligible export.",
    ]),
  ])));
}

function publicationList(payload: PublicationPayload): HTMLElement {
  if (!payload.items.length) {
    return element("article", { className: "notice" }, [
      element("strong", {}, ["No persisted publications matched"]),
      element("p", {}, ["Search currently filters locally stored publication titles only."]),
    ]);
  }
  return element("section", { className: "publication-section" }, [
    element("div", { className: "section-heading" }, [
      element("div", {}, [
        element("p", { className: "eyebrow" }, ["Persisted publications"]),
        element("h2", {}, [`${payload.total} stored match(es)`]),
      ]),
      badge(payload.mode, "neutral"),
    ]),
    element("div", { className: "cards" }, payload.items.map((item) => publicationCard(item))),
    element("p", { className: "fineprint" }, [payload.disclaimer]),
  ]);
}

function publicationCard(item: PublicationItem): HTMLElement {
  const syntheticLabel = item.synthetic === true
    ? "synthetic"
    : item.synthetic === false ? "not synthetic" : "synthetic unknown";
  const syntheticTone = item.synthetic === true ? "warn" : item.synthetic === false ? "ok" : "neutral";
  return element("article", { className: "record-card" }, [
    element("div", { className: "card-top" }, [
      badge(`origin: ${item.origin}`, item.origin === "provider" ? "ok" : item.origin === "synthetic" ? "warn" : "neutral"),
      badge(syntheticLabel, syntheticTone),
      badge(`revision ${item.revision}`, "neutral"),
    ]),
    element("h3", {}, [item.title]),
    element("p", {}, [
      [item.journal, item.publication_date].filter(Boolean).join(" · ") || "No journal/date metadata",
    ]),
    element("dl", { className: "record-meta" }, [
      meta("Identifier", item.identifier),
      meta("Provider", item.provenance.source_provider),
      meta("Source ID", item.provenance.source_identifier),
      meta("Parser", item.provenance.parser_version),
      meta("Retrieved", item.provenance.retrieved_at),
      meta("Retraction", item.retraction_status),
    ]),
    link("Open source record", item.provenance.source_url, "source-link"),
  ]);
}

function originLegend(): HTMLElement {
  return element("div", { className: "legend", ariaLabel: "Origin legend" }, [
    badge("synthetic = teaching/test data", "warn"),
    badge("provider = retrieval boundary", "ok"),
    badge("unknown = not certified", "neutral"),
  ]);
}

function sourceCard(name: string, description: string): HTMLElement {
  return element("article", { className: "record-card compact" }, [
    element("h3", {}, [name]),
    element("p", {}, [description]),
  ]);
}

function metric(label: string, value: string): HTMLElement {
  return element("div", { className: "metric" }, [
    element("span", {}, [label]),
    element("strong", {}, [value]),
  ]);
}

function meta(label: string, value: string | number | null | undefined): HTMLElement {
  return element("div", {}, [
    element("dt", {}, [label]),
    element("dd", {}, [String(value ?? "unknown")]),
  ]);
}

function offlineNotice(message: string): HTMLElement {
  return element("article", { className: "notice warn" }, [
    element("strong", {}, [message]),
    element("p", {}, ["Start the local FastAPI service to inspect live API responses."]),
  ]);
}

function resultRegion(): HTMLDivElement {
  const result = document.querySelector<HTMLDivElement>("#result");
  if (!result) throw new Error("Result region is missing");
  return result;
}

async function fetchJson<T>(path: string): Promise<{ ok: true; data: T } | { ok: false }> {
  try {
    const response = await fetch(path, { headers: { Accept: "application/json" } });
    if (!response.ok) return { ok: false };
    return { ok: true, data: await response.json() as T };
  } catch {
    return { ok: false };
  }
}

function actionButton(label: string, view: string, handler: () => void | Promise<void>): HTMLButtonElement {
  const button = element("button", { type: "button", dataView: view }, [label]);
  button.addEventListener("click", () => {
    void handler();
  });
  return button;
}

function input(id: string, value: string): HTMLInputElement {
  const field = document.createElement("input");
  field.id = id;
  field.value = value;
  field.maxLength = 120;
  field.autocomplete = "off";
  return field;
}

function badge(text: string, tone: "ok" | "warn" | "neutral"): HTMLElement {
  return element("span", { className: `badge ${tone}` }, [text]);
}

function link(text: string, href: string, className?: string): HTMLAnchorElement {
  const anchor = document.createElement("a");
  anchor.textContent = text;
  anchor.href = href;
  anchor.rel = "noreferrer";
  if (className) anchor.className = className;
  return anchor;
}

function element<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  props: Partial<HTMLElementTagNameMap[K]> & Record<string, unknown> = {},
  children: Array<Node | string> = [],
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value == null) continue;
    if (key === "className") node.className = String(value);
    else if (key === "htmlFor" && node instanceof HTMLLabelElement) node.htmlFor = String(value);
    else if (key === "ariaLabel") node.setAttribute("aria-label", String(value));
    else if (key === "ariaLive") node.setAttribute("aria-live", String(value));
    else if (key === "dataView") node.dataset.view = String(value);
    else if (key in node) {
      (node as unknown as Record<string, unknown>)[key] = value;
    } else {
      node.setAttribute(key, String(value));
    }
  }
  node.append(...children);
  return node;
}

function formatNumber(value: number): string {
  return Number.isFinite(value) ? value.toFixed(2) : "n/a";
}
