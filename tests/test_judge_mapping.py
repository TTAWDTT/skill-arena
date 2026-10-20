from skill_arena.evaluate import preference_for_skill


def test_preference_mapping():
    assert preference_for_skill("B", "A=baseline,B=skill") == "win"
    assert preference_for_skill("A", "A=baseline,B=skill") == "lose"
    assert preference_for_skill("A", "A=skill,B=baseline") == "win"
    assert preference_for_skill("tie", "A=baseline,B=skill") == "tie"
