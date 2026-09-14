type EvidenceSummary = { records: number; active_records: number; mean_confidence: number; disclaimer: string };

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("Dashboard root is missing");

app.innerHTML = `
  <header><p class="eyebrow">OPEN SCIENCE · RESEARCH INFRASTRUCTURE</p><h1>OpenLongevity</h1>
  <p>Evidence mapping for biological aging research.</p></header>
  <section class="search"><label for="topic">Explore a topic</label><input id="topic" value="cellular senescence" maxlength="120"><button id="run">Inspect evidence</button></section>
  <section id="result" aria-live="polite"><p>Results retain provenance and distinguish study designs.</p></section>
  <footer>Research use only. Not medical advice.</footer>`;

const result = document.querySelector<HTMLDivElement>("#result");
document.querySelector<HTMLButtonElement>("#run")?.addEventListener("click", async () => {
  const topic = document.querySelector<HTMLInputElement>("#topic")?.value.trim() ?? "";
  if (!topic || !result) return;
  result.textContent = "Loading evidence summary…";
  try {
    const response = await fetch(`/api/v1/evidence?topic=${encodeURIComponent(topic)}`);
    if (!response.ok) throw new Error("API request failed");
    const payload = (await response.json()) as { summary: EvidenceSummary };
    result.innerHTML = `<h2>Evidence summary</h2><p>${payload.summary.active_records} active record(s), mean confidence ${payload.summary.mean_confidence}</p><small>${payload.summary.disclaimer}</small>`;
  } catch {
    result.textContent = "The API is unavailable. Start the local FastAPI service to explore fixtures.";
  }
});
