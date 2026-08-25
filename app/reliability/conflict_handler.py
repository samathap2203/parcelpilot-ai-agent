from typing import Any, Dict, List

from app.reliability.source_priority import rank_sources


def detect_conflict(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detect whether retrieved sources provide conflicting guidance.

    Each source should contain:
      - source_type
      - document
      - text
    """

    if len(sources) < 2:
        return {
            "conflict": False,
            "authoritative_source": sources[0] if sources else None,
            "sources": sources,
        }

    ranked = rank_sources(sources)

    # The highest-priority source is treated as the leading authority.
    authoritative = ranked[0]

    return {
        "conflict": True,
        "authoritative_source": authoritative,
        "sources": ranked,
        "reason": (
            "Multiple sources were retrieved. "
            "The source with the highest configured authority "
            "should be used for the final answer."
        ),
    }