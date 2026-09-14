type EvidenceSummary = { records: number; active_records: number; mean_confidence: number; mean_navigation_score?: number; disclaimer: string };
type SearchPayload = { items: Array<Record<string, unknown>>; total: number };

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("Dashboard root is missing");

app.innerHTML = `
  <header><p class="eyebrow">OPEN SCIENCE · RESEARCH INFRASTRUCTURE · v0.2.0</p><h1>OpenLongevity</h1>
  <p>Evidence mapping for biological aging research.</p><nav aria-label="Primary"><button data-view="evidence">Evidence</button><button data-view="graph">Knowledge graph</button><button data-view="sources">Sources</button></nav></header>
  <main><section class="search"><label for="topic">Explore a topic</label><div><input id="topic" value="cellular senescence" maxlength="120"><button id="run">Inspect evidence</button></div><p class="status" id="status">API status: checking…</p></section>
  <section id="result" aria-live="polite"><p>Results retain provenance and distinguish study designs.</p></section></main>
  <footer class="site-footer"><div><strong>OpenLongevity</strong><span>Open science for a healthier tomorrow</span></div><div><strong>Ciprian Ștefan Pleșca</strong><span>Founder · Principal Author · Lead Maintainer</span></div><div><a href="https://github.com/Ciprian-LocalPulse/OpenLongevityLab">GitHub</a><a href="/WHITEPAPER.md">Whitepaper</a><a href="/ACADEMIC_MANIFESTO.md">Academic manifesto</a></div><small>Research use only · Not medical advice · v0.2.0</small></footer>`;

const result = document.querySelector<HTMLDivElement>("#result");
document.querySelector<HTMLButtonElement>("#run")?.addEventListener("click", async () => {
  const topic = document.querySelector<HTMLInputElement>("#topic")?.value.trim() ?? "";
  if (!topic || !result) return;
  result.textContent = "Loading evidence summary…";
  try {
    const response = await fetch(`/api/v1/evidence?topic=${encodeURIComponent(topic)}`);
    if (!response.ok) throw new Error("API request failed");
    const payload = (await response.json()) as { summary: EvidenceSummary };
    result.innerHTML = `<h2>Evidence summary</h2><p>${payload.summary.active_records} active record(s), mean confidence ${payload.summary.mean_confidence}; navigation score ${payload.summary.mean_navigation_score ?? "n/a"}</p><small>${payload.summary.disclaimer}</small>`;
    const search = await fetch(`/api/v1/search?query=${encodeURIComponent(topic)}&limit=10`);
    if (search.ok) {
      const data = (await search.json()) as SearchPayload;
      result.innerHTML += `<h3>Mapped resources (${data.total})</h3><ul>${data.items.map((item) => `<li><strong>${String(item.title ?? item.name ?? item.id)}</strong> <span class="badge">${String(item.type ?? item.kind ?? "resource")}</span></li>`).join("")}</ul>`;
    }
  } catch {
    result.textContent = "The API is unavailable. Start the local FastAPI service to explore fixtures.";
  }
});

document.querySelectorAll<HTMLButtonElement>("[data-view]").forEach((button) => button.addEventListener("click", async () => {
  if (!result) return;
  const view = button.dataset.view;
  if (view === "graph") {
    const response = await fetch("/api/v1/graph");
    const graph = (await response.json()) as Record<string, Array<{ relation: string; object: string }>>;
    const edges = Object.entries(graph).flatMap(([subject, links]) => links.map((link) => `${subject} ${link.relation} ${link.object}`));
    result.innerHTML = `<h2>Knowledge graph</h2><p>${Object.keys(graph).length} subjects · ${edges.length} typed edges</p><ul>${edges.map((edge) => `<li>${edge}</li>`).join("")}</ul>`;
  } else if (view === "sources") {
    result.innerHTML = `<h2>Connected sources</h2><p>PubMed · Europe PMC · OpenAlex · Crossref · ClinicalTrials.gov</p><p>Each record carries a source identifier, retrieval timestamp, URL, and normalization version.</p>`;
  }
}));

fetch("/api/v1/health").then((response) => response.json()).then((health: { status: string }) => {
  const status = document.querySelector<HTMLParagraphElement>("#status");
  if (status) status.textContent = `API status: ${health.status}`;
}).catch(() => {
  const status = document.querySelector<HTMLParagraphElement>("#status");
  if (status) status.textContent = "API status: offline (run FastAPI locally)";
});
