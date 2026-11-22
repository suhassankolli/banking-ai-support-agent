
import pytest

from skill_loader import SkillLoadError, load_skill


def test_approved_skill():
    skill = load_skill("banking-support")
    assert skill.name == "banking-support"
    assert skill.instructions


def test_unapproved_skill():
    with pytest.raises(SkillLoadError):
        load_skill("unknown-skill")


def test_path_traversal():
    with pytest.raises(SkillLoadError):
        load_skill("../secrets")
