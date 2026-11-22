
from dataclasses import dataclass
from pathlib import Path

import yaml

SKILLS_DIR = Path(__file__).parent / "skills"
ALLOWED_SKILLS = {"banking-support"}


class SkillLoadError(Exception):
    pass


@dataclass(frozen=True)
class AgentSkill:
    name: str
    description: str
    instructions: str


def load_skill(name: str) -> AgentSkill:
    if name not in ALLOWED_SKILLS:
        raise SkillLoadError("Skill is not approved")

    path = SKILLS_DIR / name / "SKILL.md"

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SkillLoadError("Unable to read skill") from exc

    lines = content.splitlines()

    if not lines or lines[0].strip() != "---":
        raise SkillLoadError("Missing YAML frontmatter")

    try:
        closing_index = lines.index("---", 1)
    except ValueError as exc:
        raise SkillLoadError("Missing closing delimiter") from exc

    try:
        metadata = yaml.safe_load(
            "\n".join(lines[1:closing_index])
        )
    except yaml.YAMLError as exc:
        raise SkillLoadError("Invalid YAML") from exc

    if not isinstance(metadata, dict):
        raise SkillLoadError("Invalid metadata")

    if metadata.get("name") != name:
        raise SkillLoadError("Skill name mismatch")

    description = metadata.get("description")
    instructions = "\n".join(
        lines[closing_index + 1:]
    ).strip()

    if not isinstance(description, str):
        raise SkillLoadError("Missing description")

    if not description.strip() or not instructions:
        raise SkillLoadError("Incomplete skill")

    return AgentSkill(
        name=name,
        description=description.strip(),
        instructions=instructions,
    )
