# gaia-chain/dsl/rules/economic_rules.py

"""
Economic Rules for Gaia DSL

This module defines the core economic concepts and types used in the Gaia DSL. The DSL is a high-level, declarative
language for the GaiaChain ecosystem, enabling users to define decentralized AI agents (dAls), request services, and
express economic interactions.

The Gaia DSL is central to GaiaChain, a decentralized intelligence economy powered by the GAIA token and governed by a DAO.
This module provides the economic foundation for the DSL’s syntax, forming the backbone for service requests, payments,
and dispute resolution.

Key Components:
1. Payments
2. Service Agreements
3. Disputes
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Union, Any

# Payments

class PaymentMethod(Enum):
    """Enum for payment methods in Gaia DSL."""
    DIRECT_TRANSFER = 'direct_transfer'
    CONTRACT_CALL = 'contract_call'

@dataclass
class Payment:
    """Class representing a payment in Gaia DSL."""
    amount: float
    currency: str = 'GAIA'
    recipient: str = None  # ID of the agent or smart contract
    method: PaymentMethod = PaymentMethod.DIRECT_TRANSFER

    def validate(self) -> bool:
        """Validate the payment details."""
        if self.amount <= 0:
            raise ValueError("Payment amount must be positive.")
        if not self.recipient:
            raise ValueError("Payment recipient must be specified.")
        return True

# Service Agreements

@dataclass
class ServiceTerm:
    """Class representing a term in a service agreement."""
    key: str
    value: Any

@dataclass
class ServiceAgreement:
    """Class representing a service agreement in Gaia DSL."""
    service_id: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    cost: Payment
    compute_requirements: Dict[str, Any] = None
    sla: Dict[str, Any] = None  # Service-Level Agreements

    def validate(self) -> bool:
        """Validate the service agreement details."""
        if not self.service_id:
            raise ValueError("Service ID must be specified.")
        if not self.inputs:
            raise ValueError("Service inputs must be specified.")
        if not self.outputs:
            raise ValueError("Service outputs must be specified.")
        self.cost.validate()
        return True

# Disputes

class DisputeResolutionMethod(Enum):
    """Enum for dispute resolution methods."""
    DAO_VOTE = 'dao_vote'
    MEDIATION = 'mediation'
    ARBITRATION = 'arbitration'

@dataclass
class Dispute:
    """Class representing a dispute in Gaia DSL."""
    initiator: str  # ID of the initiator (user, agent, etc.)
    target: str  # ID of the target (agent, service, etc.)
    reason: str  # Reason for the dispute
    resolution_method: DisputeResolutionMethod
    status: str = 'pending'  # Status of the dispute (pending, resolved, etc.)

    def resolve(self, resolution: str) -> None:
        """Resolve the dispute with a given resolution."""
        self.status = 'resolved'
        self.resolution = resolution

    def escalate(self) -> None:
        """Escalate the dispute if it cannot be resolved."""
        self.status = 'escalated'

# Example usage (for illustration purposes, not part of the module)
if __name__ == "__main__":
    # Example of defining a payment
    payment = Payment(amount=5, recipient="agent_123", method=PaymentMethod.DIRECT_TRANSFER)
    payment.validate()

    # Example of defining a service agreement
    agreement = ServiceAgreement(
        service_id="DataAnalysis",
        inputs={"data": "market_data"},
        outputs={"report": "analysis_report"},
        cost=payment
    )
    agreement.validate()

    # Example of defining a dispute
    dispute = Dispute(
        initiator="user_456",
        target="agent_123",
        reason="Inaccurate output",
        resolution_method=DisputeResolutionMethod.DAO_VOTE
    )
    dispute.resolve("Recalculated with new data")