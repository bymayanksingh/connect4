"""
Backward compatibility layer for legacy agent_factory.py.
For modern development, import directly from connect4.ai.
"""
from connect4.ai.factory import make_agent, AgentFactory
from connect4.ai.dp_agent import DPAgent

__all__ = ["make_agent", "AgentFactory", "DPAgent"]
