import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize, resolve } from "node:path";
import { chromium } from "@playwright/test";

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
