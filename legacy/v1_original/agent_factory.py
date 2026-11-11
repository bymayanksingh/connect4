

"""
agent_factory.py
----------------
Centralised helper to configure and create DPAgent instances.

Edit the defaults here (γ, dp_only, verbosity) instead of hunting through
game_data.py or other files.  Any module can simply:

    from agent_factory import make_agent
    agent = make_agent()             # DP‑only, γ=0.95, quiet
    strong = make_agent(dp_only=False, gamma=0.99, verbose=True)
"""

from typing import Any

from dp_agent import DPAgent


def make_agent(
    *,
    dp_only: bool = True,
    gamma: float = 0.95,
    verbose: bool = False,
    **kwargs: Any
) -> DPAgent:
    """
    Build and return a configured DPAgent.

    Args
    ----
    dp_only   : If True  →  search & heuristics **disabled** (pure DP mode).
                If False →  search & heuristics **enabled** (strong-play mode).
    gamma     : Discount factor (0 < γ ≤ 1).
    verbose   : Master verbosity flag controlling most console prints.
    **kwargs  : Forward‑compatibility – any extra keyword args are passed
                straight to the DPAgent constructor.

    Returns
    -------
    DPAgent instance with the requested configuration.
    """
    return DPAgent(
        discount_factor=gamma,
        use_heuristics=not dp_only,
        use_search=not dp_only,
        verbose=verbose,
        **kwargs,
    )