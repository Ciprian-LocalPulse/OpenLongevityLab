"""ClinicalTrials.gov API v2 adapter (read-only)."""

from datetime import UTC, datetime

from .base import ClinicalTrial, Provenance, ProviderError, SearchQuery
from .http import request_json


class ClinicalTrialsProvider:
    name = "clinicaltrials.gov"
    _endpoint = "https://clinicaltrials.gov/api/v2/studies"

    async def search(self, query: SearchQuery) -> list[ClinicalTrial]:
        payload = await request_json(
            self._endpoint,
            params={"query.term": query.query, "pageSize": query.limit, "format": "json"},
        )
        studies = payload.get("studies", [])
        if not isinstance(studies, list):
            raise ProviderError("ClinicalTrials.gov returned malformed studies")
        return [trial for item in studies if (trial := self._parse(item)) is not None]

    async def get_by_id(self, external_id: str) -> ClinicalTrial | None:
        payload = await request_json(f"{self._endpoint}/{external_id}", params={"format": "json"})
        return self._parse(payload)

    def _parse(self, study: dict) -> ClinicalTrial | None:
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        nct_id = identification.get("nctId")
        title = identification.get("briefTitle")
        if not nct_id or not title:
            return None
        status = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        sponsor = protocol.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name")
        interventions = tuple(
            item.get("name", "")
            for item in protocol.get("armsInterventionsModule", {}).get("interventions", [])
            if item.get("name")
        )
        outcomes = tuple(
            item.get("measure", "")
            for item in protocol.get("outcomesModule", {}).get("primaryOutcomes", [])
            if item.get("measure")
        )
        locations = tuple(
            ", ".join(filter(None, (item.get("city"), item.get("country"))))
            for item in protocol.get("contactsLocationsModule", {}).get("locations", [])
        )
        return ClinicalTrial(
            nct_id=nct_id,
            title=title,
            official_title=identification.get("officialTitle"),
            phase=tuple(design.get("phases", [])),
            status=status.get("overallStatus"),
            sponsor=sponsor,
            enrollment=design.get("enrollmentInfo", {}).get("count"),
            interventions=interventions,
            conditions=tuple(protocol.get("conditionsModule", {}).get("conditions", [])),
            outcomes=outcomes,
            locations=tuple(item for item in locations if item),
            start_date=status.get("startDateStruct", {}).get("date"),
            completion_date=status.get("completionDateStruct", {}).get("date"),
            provenance=Provenance(
                "clinicaltrials.gov",
                nct_id,
                f"https://clinicaltrials.gov/study/{nct_id}",
                datetime.now(UTC).isoformat(),
            ),
        )
