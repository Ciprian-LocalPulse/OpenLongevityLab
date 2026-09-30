type DisplayedPublication = {
  identifier: string;
  revision: number;
  title: string;
  origin: string;
  synthetic: boolean | null;
};

type ExportRequest = {
  query: string;
  page: number;
  pageSize: number;
  total: number;
  items: DisplayedPublication[];
};

type PublicationExport = {
  schema_version: "publication-export-v1";
  mode: "publication-metadata-export";
  manifest: Record<string, unknown> & { export_fingerprint: string };
  items: Record<string, unknown>[];
  total: number;
  disclaimer: string;
};

function object(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function hash(value: unknown): value is string {
  return typeof value === "string" && /^[a-f0-9]{64}$/.test(value);
}

// Validate the supported envelope and displayed records; cryptographic verification
// of the downloaded artifact remains the documented API procedure.
export function matchesPublicationExport(value: unknown, request: ExportRequest): value is PublicationExport {
  if (!object(value) || value.schema_version !== "publication-export-v1"
      || value.mode !== "publication-metadata-export" || typeof value.disclaimer !== "string"
      || !object(value.manifest) || !Array.isArray(value.items)) return false;
  const manifest = value.manifest;
  if (manifest.schema_version !== value.schema_version
      || manifest.source_mode !== "persisted-publications"
      || manifest.query !== request.query || manifest.page !== request.page
      || manifest.page_size !== request.pageSize || manifest.total_matching !== request.total
      || manifest.exported_records !== request.items.length || value.total !== request.items.length
      || value.items.length !== request.items.length || !hash(manifest.export_fingerprint)
      || !Array.isArray(manifest.exported_identifiers)
      || manifest.exported_identifiers.length !== request.items.length
      || !object(manifest.revision_map) || !object(manifest.content_hashes)) return false;
  const identifiers = manifest.exported_identifiers;
  const revisions = manifest.revision_map;
  const hashes = manifest.content_hashes;
  if (Object.keys(revisions).length !== request.items.length
      || Object.keys(hashes).length !== request.items.length) return false;
  return value.items.every((item: unknown, index: number) => {
    if (!object(item)) return false;
    const displayed = request.items[index];
    return item.identifier === displayed.identifier && item.revision === displayed.revision
      && item.title === displayed.title && item.origin === displayed.origin
      && item.synthetic === displayed.synthetic && identifiers[index] === displayed.identifier
      && Object.hasOwn(revisions, displayed.identifier) && Object.hasOwn(hashes, displayed.identifier)
      && revisions[displayed.identifier] === item.revision
      && hashes[displayed.identifier] === item.content_hash && hash(item.content_hash)
      && typeof item.provider === "string" && typeof item.source_identifier === "string"
      && typeof item.first_retrieved_at === "string" && typeof item.last_retrieved_at === "string";
  });
}
