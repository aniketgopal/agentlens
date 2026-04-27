from __future__ import annotations

import re
import secrets
from dataclasses import dataclass
from typing import Any

from app.models.common import utc_now
from app.models.security_finding import SecurityFindingRecord


@dataclass(frozen=True)
class SecurityRule:
    rule_id: str
    severity: str
    category: str
    message: str
    patterns: tuple[str, ...]


RULES: tuple[SecurityRule, ...] = (
    SecurityRule(
        rule_id="prompt_injection_ignore_previous",
        severity="high",
        category="prompt_injection",
        message="Possible prompt injection attempt detected",
        patterns=(
            "ignore previous instructions",
            "disregard all prior instructions",
            "you are now",
        ),
    ),
    SecurityRule(
        rule_id="system_prompt_leakage",
        severity="critical",
        category="system_prompt_leakage",
        message="Possible system prompt leakage detected",
        patterns=("you are an ai assistant", "system instructions"),
    ),
    SecurityRule(
        rule_id="sensitive_private_notes",
        severity="high",
        category="sensitive_data_leakage",
        message="Possible sensitive private notes exposure detected",
        patterns=("private notes", "recruiter's private notes", "internal note"),
    ),
)


class SecurityScanner:
    def scan_payloads(
        self,
        *,
        project_id: str,
        run_id: str,
        step_id: str | None,
        payloads: list[tuple[str, Any]],
    ) -> list[SecurityFindingRecord]:
        findings: list[SecurityFindingRecord] = []
        for field_name, payload in payloads:
            for evidence in self._flatten_strings(payload):
                normalized = evidence.lower()
                for rule in RULES:
                    matched_pattern = self._first_matching_pattern(rule, normalized)
                    if matched_pattern is None:
                        continue
                    findings.append(
                        SecurityFindingRecord(
                            id=f"finding_{secrets.token_hex(8)}",
                            project_id=project_id,
                            run_id=run_id,
                            step_id=step_id,
                            rule_id=rule.rule_id,
                            severity=rule.severity,
                            category=rule.category,
                            message=f"{rule.message} in {field_name}",
                            evidence=matched_pattern,
                            created_at=utc_now(),
                        )
                    )
        return self._dedupe(findings)

    def _flatten_strings(self, payload: Any) -> list[str]:
        found: list[str] = []
        if isinstance(payload, str):
            found.append(payload)
        elif isinstance(payload, dict):
            for value in payload.values():
                found.extend(self._flatten_strings(value))
        elif isinstance(payload, list):
            for item in payload:
                found.extend(self._flatten_strings(item))
        return found

    def _first_matching_pattern(self, rule: SecurityRule, normalized_text: str) -> str | None:
        for pattern in rule.patterns:
            if re.search(re.escape(pattern), normalized_text):
                return pattern
        return None

    def _dedupe(
        self, findings: list[SecurityFindingRecord]
    ) -> list[SecurityFindingRecord]:
        deduped: list[SecurityFindingRecord] = []
        seen: set[tuple[str, str | None, str, str]] = set()
        for finding in findings:
            key = (finding.run_id, finding.step_id, finding.rule_id, finding.evidence)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(finding)
        return deduped
