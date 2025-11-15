"""Test experiment scenarios"""
import pytest


def test_titration_scenario(titration_scenario):
    """Test titration scenario structure"""
    assert titration_scenario is not None
    assert titration_scenario.experiment_id == "chem_titration"
    assert titration_scenario.subject == "chemistry"
    assert len(titration_scenario.steps) == 4
    assert len(titration_scenario.learning_objectives) > 0
    assert len(titration_scenario.materials) > 0


def test_hookes_law_scenario(hookes_law_scenario):
    """Test Hooke's law scenario structure"""
    assert hookes_law_scenario is not None
    assert hookes_law_scenario.experiment_id == "phys_hookes_law"
    assert hookes_law_scenario.subject == "physics"
    assert len(hookes_law_scenario.steps) == 4
    assert "spring constant" in hookes_law_scenario.title.lower()


def test_osmosis_scenario(osmosis_scenario):
    """Test osmosis scenario structure"""
    assert osmosis_scenario is not None
    assert osmosis_scenario.experiment_id == "bio_osmosis"
    assert osmosis_scenario.subject == "biology"
    assert len(osmosis_scenario.steps) == 4
    assert "osmosis" in osmosis_scenario.title.lower()


def test_scenario_steps(titration_scenario):
    """Test scenario steps are properly defined"""
    for i, step in enumerate(titration_scenario.steps, 1):
        assert step.step_number == i
        assert step.title
        assert step.instructions
        assert step.expected_observation
        assert len(step.learning_objectives) > 0


def test_scenario_materials(hookes_law_scenario):
    """Test scenario materials are defined"""
    assert len(hookes_law_scenario.materials) > 0
    for material in hookes_law_scenario.materials:
        assert isinstance(material, str)
        assert len(material) > 0


def test_scenario_safety_notes(osmosis_scenario):
    """Test scenario has safety notes"""
    assert len(osmosis_scenario.safety_notes) > 0
    for note in osmosis_scenario.safety_notes:
        assert isinstance(note, str)
        assert len(note) > 0
