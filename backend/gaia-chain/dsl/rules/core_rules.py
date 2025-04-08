# gaia-chain/dsl/rules/core_rules.py

"""
Core Rules for Gaia DSL

This module defines the core concepts and types used in the Gaia DSL. The DSL is a high-level, declarative language
for the GaiaChain ecosystem, enabling users to define decentralized AI agents (dAls), request services, and express
economic interactions.

The Gaia DSL is central to GaiaChain, a decentralized intelligence economy powered by the GAIA token and governed by a DAO.
This module provides the semantic foundation for the DSL’s syntax, forming the backbone for agent execution, service
processing, and governance.

Key Components:
1. Basic Data Types
2. Core Actions or Commands
3. Core Logical Operators
"""

from enum import Enum
from dataclasses import dataclass
from typing import Union, List, Dict, Any

# Basic Data Types

class GaiaType(Enum):
    """Enum for basic data types in Gaia DSL."""
    INTEGER = 'integer'
    STRING = 'string'
    FLOAT = 'float'
    BOOLEAN = 'boolean'
    AGENT_ID = 'agent_id'
    TOKEN_AMOUNT = 'token_amount'
    CONDITION = 'condition'

@dataclass
class GaiaValue:
    """Class representing a value in Gaia DSL."""
    type: GaiaType
    value: Any

@dataclass
class AgentProperty:
    """Class representing an agent property."""
    name: str
    value: GaiaValue

@dataclass
class ServiceInputOutput:
    """Class representing input or output for a service."""
    name: str
    value: GaiaValue

@dataclass
class EconomicValue:
    """Class representing an economic value, e.g., GAIA tokens."""
    amount: float
    currency: str = 'GAIA'

# Core Actions or Commands

class GaiaAction(Enum):
    """Enum for core actions or commands in Gaia DSL."""
    COMPUTE = 'compute'
    SEND_MESSAGE = 'send_message'
    CALL_CONTRACT = 'call_contract'
    REQUEST_SERVICE = 'request_service'

@dataclass
class Action:
    """Class representing an action in Gaia DSL."""
    action_type: GaiaAction
    parameters: Dict[str, GaiaValue]

def compute(model: str, data: GaiaValue) -> Action:
    """Define a compute action."""
    return Action(
        action_type=GaiaAction.COMPUTE,
        parameters={'model': GaiaValue(GaiaType.STRING, model), 'data': data}
    )

def send_message(message: str, recipient: str) -> Action:
    """Define a send message action."""
    return Action(
        action_type=GaiaAction.SEND_MESSAGE,
        parameters={'message': GaiaValue(GaiaType.STRING, message), 'recipient': GaiaValue(GaiaType.STRING, recipient)}
    )

def call_contract(contract: str, function: str, params: Dict[str, GaiaValue]) -> Action:
    """Define a call contract action."""
    return Action(
        action_type=GaiaAction.CALL_CONTRACT,
        parameters={'contract': GaiaValue(GaiaType.STRING, contract), 'function': GaiaValue(GaiaType.STRING, function), 'params': params}
    )

def request_service(service_id: str, inputs: List[ServiceInputOutput], payment: EconomicValue, constraints: List[AgentProperty]) -> Action:
    """Define a request service action."""
    return Action(
        action_type=GaiaAction.REQUEST_SERVICE,
        parameters={
            'service_id': GaiaValue(GaiaType.STRING, service_id),
            'inputs': GaiaValue(GaiaType.STRING, str(inputs)),  # Simplified for example
            'payment': GaiaValue(GaiaType.TOKEN_AMOUNT, payment),
            'constraints': GaiaValue(GaiaType.STRING, str(constraints))  # Simplified for example
        }
    )

# Core Logical Operators

class LogicalOperator(Enum):
    """Enum for logical operators."""
    EQUAL = '='
    GREATER_THAN = '>'
    LESS_THAN = '<'
    AND = 'and'
    OR = 'or'

@dataclass
class Condition:
    """Class representing a condition in Gaia DSL."""
    left: GaiaValue
    operator: LogicalOperator
    right: GaiaValue

def evaluate_condition(condition: Condition) -> bool:
    """Evaluate a condition."""
    if condition.operator == LogicalOperator.EQUAL:
        return condition.left.value == condition.right.value
    elif condition.operator == LogicalOperator.GREATER_THAN:
        return condition.left.value > condition.right.value
    elif condition.operator == LogicalOperator.LESS_THAN:
        return condition.left.value < condition.right.value
    elif condition.operator == LogicalOperator.AND:
        return condition.left.value and condition.right.value
    elif condition.operator == LogicalOperator.OR:
        return condition.left.value or condition.right.value
    else:
        raise ValueError(f"Unsupported operator: {condition.operator}")

# Example usage (for illustration purposes, not part of the module)
if __name__ == "__main__":
    # Example of defining an agent property
    agent_name = AgentProperty(name="name", value=GaiaValue(type=GaiaType.STRING, value="AnalyticalAgent"))
    
    # Example of defining a compute action
    compute_action = compute(model="MLModel", data=GaiaValue(type=GaiaType.STRING, value="input_data"))
    
    # Example of defining a condition
    condition = Condition(left=GaiaValue(type=GaiaType.FLOAT, value=0.6), operator=LogicalOperator.GREATER_THAN, right=GaiaValue(type=GaiaType.FLOAT, value=0.5))
    
    # Evaluate condition
    result = evaluate_condition(condition)
    print(f"Condition result: {result}")