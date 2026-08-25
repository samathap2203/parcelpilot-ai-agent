from dataclasses import dataclass


@dataclass(frozen=True)
class SourceRule:
    source_type: str
    priority: int
    description: str


SOURCE_RULES = [
    SourceRule(
        source_type="customer_agreement",
        priority=1,
        description="Signed customer-specific agreement.",
    ),
    SourceRule(
        source_type="current_policy",
        priority=2,
        description="Current effective ParcelPilot policy or SOP.",
    ),
    SourceRule(
        source_type="current_product_documentation",
        priority=3,
        description="Current product documentation or known-issue guidance.",
    ),
    SourceRule(
        source_type="historical_ticket",
        priority=4,
        description="Historical ticket information used only as context.",
    ),
    SourceRule(
        source_type="deprecated_policy",
        priority=5,
        description="Deprecated policy retained for historical context only.",
    ),
]


def get_priority(source_type: str) -> int:
    """Return the authority priority for a source type."""

    for rule in SOURCE_RULES:
        if rule.source_type == source_type:
            return rule.priority

    return 999


def rank_sources(sources: list[dict]) -> list[dict]:
    """Rank retrieved sources by authority."""

    return sorted(
        sources,
        key=lambda source: get_priority(source.get("source_type", "")),
    )


def is_authoritative(source_type: str) -> bool:
    """Return whether the source can be treated as authoritative."""

    return source_type in {
        "customer_agreement",
        "current_policy",
        "current_product_documentation",
    }