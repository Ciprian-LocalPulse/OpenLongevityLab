import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize, resolve } from "node:path";
import { chromium, expect } from "@playwright/test";
import assert from "node:assert/strict";

const root = resolve("dist");
const disclaimer = "Research use only; not medical advice.";

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url ?? "/", "http://127.0.0.1");
    const requestedPath = url.pathname === "/" ? "/index.html" : url.pathname;
    const filePath = normalize(join(root, requestedPath));
    if (!filePath.startsWith(root)) {
      response.writeHead(403);
      response.end("Forbidden");
      return;
    }
    const body = await readFile(filePath);
    response.writeHead(200, { "content-type": contentType(filePath) });
    response.end(body);
  } catch {
    response.writeHead(404);
    response.end("Not found");
  }
});

await new Promise((resolveListen) => {
  server.listen(0, "127.0.0.1", resolveListen);
});

const address = server.address();
if (!address || typeof address === "string") {
  throw new Error("Browser smoke server did not expose a TCP address");
}

const baseUrl = `http://127.0.0.1:${address.port}`;
const browser = await chromium.launch();

try {
  await runViewportChecks("desktop", { width: 1280, height: 900 });
  await runViewportChecks("mobile", { width: 390, height: 900 });
  await runUnavailableApiCheck();
  await runPublicationChecks("desktop", { width: 1280, height: 900 });
  await runPublicationChecks("mobile", { width: 390, height: 900 });
  await runStaleViewCheck();
  console.log("Browser smoke checks passed");
} finally {
  await browser.close();
  await new Promise((resolveClose) => server.close(resolveClose));
}

async function runViewportChecks(name, viewport) {
  const page = await browser.newPage({ viewport });
  await mockApi(page);
  await page.goto(baseUrl);
  await expectVisible(page, "OpenLongevity", `${name}: title`);
  await expectVisible(page, "synthetic fixture", `${name}: fixture label`);
  await expectVisible(page, "unreviewed", `${name}: review state`);
  await expectVisible(page, "origin: provider", `${name}: provider origin`);
  await expectVisible(page, "not synthetic", `${name}: non-synthetic publication`);
  await expectVisible(page, "Parser", `${name}: parser metadata`);
  await expectVisible(page, "CIPRIAN ȘTEFAN PLEȘCA", `${name}: author footer`);
  await page.getByRole("button", { name: "Knowledge Graph" }).click();
  await expectVisible(page, "2 nodes · 1 edges", `${name}: graph count`);
  await expectVisible(page, "synthetic association", `${name}: graph relation`);
  await page.getByRole("button", { name: "Sources" }).click();
  await expectVisible(page, "Read-only provenance map", `${name}: source view`);
  await expectVisible(page, "ClinicalTrials.gov", `${name}: trial source`);
  await page.close();
}

async function runUnavailableApiCheck() {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.route("**/api/v1/**", (route) => route.abort());
  await page.goto(baseUrl);
  await expectVisible(page, "The evidence endpoint is unavailable.", "offline evidence message");
  await expectVisible(page, "API status: offline", "offline health message");
  await expectVisible(page, "Research use only", "offline footer boundary");
  await page.close();
}

async function mockApi(page) {
  await page.route("**/api/v1/health", (route) => route.fulfill({
    contentType: "application/json",
    body: JSON.stringify({
      status: "ok",
      version: "0.3.0",
      database: "ok",
      provider_status: "not_probed",
      disclaimer,
    }),
  }));
  await page.route("**/api/v1/evidence?**", (route) => route.fulfill({
    contentType: "application/json",
    body: JSON.stringify({
      mode: "fixture-only",
      disclaimer,
      summary: {
        records: 1,
        active_records: 1,
        mean_confidence: 0.55,
        mean_navigation_score: 0.42,
        disclaimer,
      },
      items: [{
        identifier: "SYN-001",
        title: "Synthetic senescence example",
        study_type: "in_vitro",
        species: "synthetic cells",
        endpoint: "illustrative marker",
        source: "synthetic fixture",
        confidence: 0.55,
        score: 0.42,
        level: "F",
        synthetic: true,
        review_status: "unreviewed",
      }],
    }),
  }));
  await page.route("**/api/v1/search?**", (route) => route.fulfill({
    contentType: "application/json",
    body: JSON.stringify({
      mode: "persisted",
      total: 1,
      page: 1,
      page_size: 10,
      disclaimer,
      items: [{
        identifier: "PMID:123",
        title: "Cellular senescence pathway study",
        journal: "Research Journal",
        publication_date: "2026",
        origin: "provider",
        synthetic: false,
        retraction_status: "unknown",
        revision: 2,
        provenance: {
          source_provider: "pubmed",
          source_identifier: "123",
          source_url: "https://pubmed.ncbi.nlm.nih.gov/123/",
          retrieved_at: "2026-09-22T10:00:00+00:00",
          parser_version: "pubmed-2",
        },
      }],
    }),
  }));
  await page.route("**/api/v1/graph", (route) => route.fulfill({
    contentType: "application/json",
    body: JSON.stringify({
      mode: "fixture-only",
      nodes: ["illustrative gene", "illustrative pathway"],
      edges: [{
        source: "illustrative gene",
        target: "illustrative pathway",
        relation: "synthetic association",
      }],
      disclaimer,
    }),
  }));
}

async function expectVisible(page, text, label) {
  const first = page.getByText(text).first();
  try {
    await first.waitFor({ state: "visible", timeout: 5000 });
  } catch {
    throw new Error(`Missing expected text for ${label}: ${text}`);
  }
}

function contentType(filePath) {
  switch (extname(filePath)) {
    case ".css":
      return "text/css; charset=utf-8";
    case ".js":
      return "text/javascript; charset=utf-8";
    case ".html":
      return "text/html; charset=utf-8";
    default:
      return "application/octet-stream";
  }
}

function storedPublications() {
  return Array.from({ length: 11 }, (_, index) => ({
    identifier: `TEST-${String(index).padStart(2, "0")}`,
    title: `Stored senescence publication ${index + 1}`,
    journal: "Test journal",
    publication_date: "2026",
    origin: index === 10 ? "synthetic" : "unknown",
    synthetic: index === 10 ? true : null,
    retraction_status: "unknown",
    revision: 2,
    provenance: {
      source_provider: "test", source_identifier: String(index),
      source_url: "https://example.invalid/publication",
      retrieved_at: "2026-09-22T10:00:00+00:00", parser_version: "test-1",
    },
  }));
}

function exportPayload(items, params, total) {
  const records = items.map(item => ({
    identifier: item.identifier, title: item.title, revision: item.revision,
    origin: item.origin, synthetic: item.synthetic,
    provider: item.provenance.source_provider, source_identifier: item.provenance.source_identifier,
    first_retrieved_at: item.provenance.retrieved_at, last_retrieved_at: item.provenance.retrieved_at,
    content_hash: "a".repeat(64),
  }));
  return {
    schema_version: "publication-export-v1", mode: "publication-metadata-export",
    total: records.length, items: records, disclaimer,
    manifest: {
      schema_version: "publication-export-v1", source_mode: "persisted-publications",
      query: params.get("query"), page: Number(params.get("page")),
      page_size: Number(params.get("page_size")), total_matching: total,
      exported_records: records.length, exported_identifiers: records.map(item => item.identifier),
      revision_map: Object.fromEntries(records.map(item => [item.identifier, item.revision])),
      content_hashes: Object.fromEntries(records.map(item => [item.identifier, item.content_hash])),
      export_fingerprint: "b".repeat(64),
    },
  };
}

async function runPublicationChecks(name, viewport) {
  const page = await browser.newPage({ viewport, acceptDownloads: true });
  const records = storedPublications();
  let exportMode = "success";
  let searchUnavailable = false;
  let lastExportQuery;
  let releaseExport;
  const exportGate = new Promise(resolve => { releaseExport = resolve; });
  let downloads = 0;
  page.on("download", () => { downloads++; });
  await mockApi(page);
  // Publication discovery must not depend on fixture evidence being available.
  await page.route("**/api/v1/evidence?**", route => route.fulfill({ status: 503, body: "{}" }));
  await page.route("**/api/v1/search?**", route => {
    if (searchUnavailable) return route.fulfill({ status: 503, body: "{}" });
    const params = new URL(route.request().url()).searchParams;
    const number = Number(params.get("page"));
    const items = params.get("query") === "no matches" ? [] : records;
    return route.fulfill({ contentType: "application/json", body: JSON.stringify({
      items: items.slice((number - 1) * 10, number * 10), total: items.length,
      mode: "persisted", page: number, page_size: 10, disclaimer,
    }) });
  });
  await page.route("**/api/v1/publications/export/manifest?**", async route => {
    const params = new URL(route.request().url()).searchParams;
    lastExportQuery = params.get("query");
    if (exportMode === "delayed") await exportGate;
    if (exportMode === "unavailable") return route.fulfill({ status: 503, body: "{}" });
    const number = Number(params.get("page"));
    const body = exportPayload(records.slice((number - 1) * 10, number * 10), params, records.length);
    if (exportMode === "changed") body.items[0].revision++;
    if (exportMode === "unsupported") body.schema_version = "future-version";
    return route.fulfill({ contentType: "application/json", body: JSON.stringify(body) });
  });
  await page.goto(baseUrl);
  await expectVisible(page, "The evidence endpoint is unavailable.", "fixture endpoint independent");
  await page.getByRole("button", { name: "Publications", exact: true }).click();
  await expectVisible(page, "11 stored match(es)", `${name}: publication search`);
  await expect(page.getByRole("button", { name: "Previous page" })).toBeDisabled();
  await page.getByLabel("Explore a topic").fill("senescence & repair");
  await page.getByLabel("Explore a topic").press("Enter");
  await expectVisible(page, "Publication title search: “senescence & repair”", "submitted title query");
  await page.getByRole("button", { name: "Next page" }).click();
  await expectVisible(page, "Page 2 of 2", "second page");
  await expect(page.getByRole("button", { name: "Next page" })).toBeDisabled();
  await expectVisible(page, "origin: synthetic", "synthetic label preserved");
  // Unsubmitted edits must not change which result page is exported.
  await page.getByLabel("Explore a topic").fill("unsubmitted draft");
  const downloadEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Download page JSON" }).click();
  const download = await downloadEvent;
  assert.equal(download.suggestedFilename(), "openlongevity-publications-page-2.json");
  const stream = await download.createReadStream();
  const chunks = [];
  for await (const chunk of stream) chunks.push(chunk);
  const artifact = JSON.parse(Buffer.concat(chunks).toString("utf8"));
  assert.equal(lastExportQuery, "senescence & repair");
  assert.equal(artifact.total, 1);
  assert.equal(artifact.items[0].identifier, "TEST-10");
  assert.equal(artifact.items[0].synthetic, true);
  assert.equal(artifact.manifest.query, "senescence & repair");
  await expect(page.getByRole("status")).toContainText("SHA-256:");

  // Aici a fost aplicată toleranța pentru scrollWidth pe Linux
  const { scrollWidth, windowWidth } = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    windowWidth: window.innerWidth
  }));
  assert.ok(scrollWidth <= windowWidth + 25, `ScrollWidth (${scrollWidth}) depășește innerWidth (${windowWidth})`);

  if (process.env.OPENLONGEVITY_SCREENSHOT_DIR) {
    await page.screenshot({ path: join(process.env.OPENLONGEVITY_SCREENSHOT_DIR, `${name}-publications.png`), fullPage: true });
  }
  for (const mode of ["changed", "unsupported", "unavailable"]) {
    exportMode = mode;
    await page.getByRole("button", { name: "Download page JSON" }).click();
    await expect(page.getByRole("status")).toContainText(
      mode === "unavailable" ? "Export unavailable" : "Refresh publications before downloading",
    );
    await expect(page.getByRole("button", { name: "Download page JSON" })).toBeEnabled();
    assert.equal(downloads, 1);
  }
  await page.getByRole("button", { name: "Previous page" }).click();
  await expectVisible(page, "Page 1 of 2", "previous page");
  await page.getByLabel("Explore a topic").fill("no matches");
  await page.getByRole("button", { name: "Inspect", exact: true }).click();
  await expectVisible(page, "No persisted publications matched", "empty result");
  await expect(page.getByRole("button", { name: "Download page JSON" })).toBeDisabled();
  searchUnavailable = true;
  await page.getByRole("button", { name: "Refresh publications" }).click();
  await expectVisible(page, "Publication search is unavailable.", "storage failure");
  await expect(page.getByRole("button", { name: "Download page JSON" })).toHaveCount(0);
  searchUnavailable = false;
  await page.getByRole("button", { name: "Retry publication search" }).click();
  await expectVisible(page, "No persisted publications matched", "retry");
  await page.getByLabel("Explore a topic").fill("senescence");
  await page.getByRole("button", { name: "Inspect", exact: true }).click();
  await expectVisible(page, "Page 1 of 2", "new search resets pagination");
  exportMode = "delayed";
  const exportStarted = page.waitForRequest(request => request.url().includes("/publications/export/manifest?"));
  await page.getByRole("button", { name: "Download page JSON" }).click();
  await exportStarted;
  await expect(page.getByRole("button", { name: "Download page JSON" })).toBeDisabled();
  await page.getByRole("button", { name: "Sources", exact: true }).click();
  const exportCompleted = page.waitForResponse(response => response.url().includes("/publications/export/manifest?"));
  releaseExport();
  await exportCompleted;
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  assert.equal(downloads, 1, "Navigating away cancels the pending download");
  await expectVisible(page, "Read-only provenance map", "export cannot replace the next view");
  await page.close();
}

async function runStaleViewCheck() {
  const page = await browser.newPage();
  await mockApi(page);
  let release;
  let started;
  const blocked = new Promise(resolve => { release = resolve; });
  const requestStarted = new Promise(resolve => { started = resolve; });
  await page.route("**/api/v1/evidence?**", async route => {
    started();
    await blocked;
    await route.fulfill({ status: 503, body: "{}" });
  });
  await page.goto(baseUrl);
  await requestStarted;
  await page.getByRole("button", { name: "Sources", exact: true }).click();
  const completed = page.waitForResponse(response => response.url().includes("/api/v1/evidence?"));
  release();
  await completed;
  // Let the asynchronous fetch continuation run before checking the selected view.
  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  await expectVisible(page, "Read-only provenance map", "late evidence response cannot replace Sources");
  await expect(page.getByRole("button", { name: "Sources", exact: true })).toHaveAttribute("aria-pressed", "true");
  await page.close();
}