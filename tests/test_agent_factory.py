import pytest

from connect4.ai.dp_agent import DPAgent
from connect4.ai.factory import AgentFactory, make_agent
from connect4.ai.heuristic_agent import HeuristicAgent
from connect4.ai.minimax import MinimaxAgent
from connect4.ai.random_agent import RandomAgent
from connect4.types import AIDifficulty


def test_factory_creates_all_difficulties():
    a_rnd = AgentFactory.create_agent("random")
    assert isinstance(a_rnd, RandomAgent)

    a_easy = AgentFactory.create_agent("easy")
    assert isinstance(a_easy, HeuristicAgent)

    a_med = AgentFactory.create_agent("medium")
    assert isinstance(a_med, MinimaxAgent)
    assert a_med.depth == 3

    a_hard = AgentFactory.create_agent("hard")
    assert isinstance(a_hard, MinimaxAgent)
    assert a_hard.depth == 5

    a_expert = AgentFactory.create_agent("expert", horizon=2, verbose=False)
    assert isinstance(a_expert, DPAgent)


def test_factory_enum_argument():
    agent = AgentFactory.create_agent(AIDifficulty.HARD)
    assert isinstance(agent, MinimaxAgent)


def test_factory_unknown_difficulty_raises():
    with pytest.raises(ValueError):
        AgentFactory.create_agent("superhuman_quantum_ai")


def test_legacy_make_agent_helper():
    agent = make_agent(dp_only=True, gamma=0.9, verbose=False)
    assert isinstance(agent, DPAgent)
    assert agent.gamma == 0.9
