from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl


class Category(str, Enum):
    coding = "coding"
    review = "review"
    writing = "writing"
    slides = "slides"
    data = "data"
    research = "research"
    other = "other"


class SkillRecord(BaseModel):
    """Unified skill schema for catalog entries."""

    skill_id: str
    name: str
    description: str = ""
    body: str = ""
    source_url: str
    source_repo: str = ""
    source_path: str = ""
    author: str = ""
    license: str = ""
    category: Category = Category.other
    tags: list[str] = Field(default_factory=list)
    trigger_description: str = ""
    body_hash: str
    collected_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at_remote: Optional[str] = None
    coarse_score: float = 0.0
    coarse_notes: list[str] = Field(default_factory=list)
    has_examples: bool = False
    structure_ok: bool = False
    excluded_reason: Optional[str] = None
    meta: dict[str, Any] = Field(default_factory=dict)


class TaskSpec(BaseModel):
    task_id: str
    category: Category
    title: str
    prompt: str
    expected_behavior: str
    scoring_rubric: list[str]
    rule_checkable: bool = False
    rule_checks: list[dict[str, Any]] = Field(default_factory=list)
    tests: list[dict[str, Any]] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class RunAttempt(BaseModel):
    attempt: int
    condition: Literal["baseline", "with_skill"]
    model: str
    skill_id: Optional[str] = None
    prompt: str
    response_text: str = ""
    raw_response: dict[str, Any] = Field(default_factory=dict)
    latency_ms: int = 0
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    error: Optional[str] = None
    triggered: Optional[bool] = None
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class JudgeVerdict(BaseModel):
    task_id: str
    skill_id: str
    pair_id: str
    order: Literal["A=baseline,B=skill", "A=skill,B=baseline"]
    winner: Literal["A", "B", "tie"]
    preference_for_skill: Literal["win", "lose", "tie"]
    rationale: str = ""
    scores: dict[str, Any] = Field(default_factory=dict)
    judge_model: str
    raw: dict[str, Any] = Field(default_factory=dict)


class PairResult(BaseModel):
    task_id: str
    skill_id: str
    baseline_attempts: list[RunAttempt]
    skill_attempts: list[RunAttempt]
    judge_verdicts: list[JudgeVerdict] = Field(default_factory=list)
    test_pass_baseline: Optional[float] = None
    test_pass_skill: Optional[float] = None
    trigger_success_rate: Optional[float] = None
    skill_win_rate: Optional[float] = None
