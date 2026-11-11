from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from connect4.ai.base import Agent
from connect4.ai.heuristic_agent import HeuristicAgent
from connect4.ai.minimax import MinimaxAgent
from connect4.ai.random_agent import RandomAgent
from connect4.ai.dp_agent import DPAgent
from connect4.types import AIDifficulty


class AgentFactory:
    """
    Centralized factory for creating and configuring Connect 4 AI agents.
    """

    @staticmethod
    def create_agent(
        difficulty: Union[AIDifficulty, str] = AIDifficulty.MEDIUM,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> Agent:
        """
        Builds and returns an Agent instance based on difficulty or algorithm name.
        """
        if isinstance(difficulty, AIDifficulty):
            key = difficulty.value.lower()
        else:
            key = str(difficulty).lower().strip()

        if key in ("random", "very_easy"):
            return RandomAgent(name=name or "Random AI")
        elif key in ("easy", "heuristic"):
            return HeuristicAgent(name=name or "Heuristic AI")
        elif key in ("medium", "minimax_medium"):
            depth = kwargs.get("depth", 3)
            return MinimaxAgent(depth=depth, name=name or f"Minimax (Depth {depth})")
        elif key in ("hard", "minimax", "minimax_hard"):
            depth = kwargs.get("depth", 5)
            return MinimaxAgent(depth=depth, name=name or f"Minimax (Depth {depth})")
        elif key in ("expert", "dp", "dp_agent", "deep"):
            gamma = kwargs.get("gamma", 0.95)
            verbose = kwargs.get("verbose", False)
            horizon = kwargs.get("horizon", 6)
            return DPAgent(
                discount_factor=gamma,
                verbose=verbose,
                horizon=horizon,
                use_heuristics=kwargs.get("use_heuristics", True),
                use_search=kwargs.get("use_search", False),
            )
        else:
            raise ValueError(
                f"Unknown AI difficulty or agent type: '{key}'. "
                f"Available: 'random', 'easy', 'medium', 'hard', 'expert'."
            )

    @staticmethod
    def available_agents() -> List[str]:
        return ["random", "easy", "medium", "hard", "expert"]


def make_agent(*args, **kwargs):
    """Backward compatibility helper matching legacy agent_factory.py."""
    if "dp_only" in kwargs:
        dp_only = kwargs.pop("dp_only")
        kwargs["use_heuristics"] = not dp_only
        kwargs["use_search"] = not dp_only
    return AgentFactory.create_agent(difficulty=AIDifficulty.EXPERT, **kwargs)
