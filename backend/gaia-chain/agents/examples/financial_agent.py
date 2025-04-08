# gaia-chain/agents/examples/financial_agent.py

"""
Financial Agent for GaiaChain

This module defines a basic financial agent demonstrating financial tasks within the GaiaChain ecosystem.
The agent leverages the core agent logic and symbolic reasoning to perform tasks such as understanding financial agreements,
requesting market data, making market predictions, and reporting results.
"""

from gaia_chain.agents.runtime.agent_core import AgentCore, AgentLifecycleEvent
from gaia_chain.agents.neuro_symbolic.symbolic_reasoner import SymbolicReasoner, Fact, Rule, Goal
import logging

logger = logging.getLogger(__name__)

class FinancialAgent(AgentCore):
    def __init__(self, id: str, owner: str):
        super().__init__(id, owner)
        self.reasoner = SymbolicReasoner()
    
    def understand_agreement(self, agreement_text: str):
        # Parse the financial agreement terms (mock implementation)
        logger.info(f"Understanding financial agreement: {agreement_text}")
        terms = agreement_text.split()
        for term in terms:
            self.reasoner.kb.add_fact(Fact(f"term: {term}"))
    
    def request_market_data(self):
        # Request market data from a service (mock implementation)
        service_id = "MarketDataService"
        payment = 10  # Mock payment in GAIA tokens
        constraints = {"data_type": "market_prices"}
        self.request_service(service_id, payment, constraints)
    
    def make_market_prediction(self):
        # Make a market prediction (mock implementation)
        logger.info("Making market prediction...")
        self.reasoner.update_knowledge(
            facts=[Fact("stock_price > 100")],
            rules=[Rule(["stock_price > 100"], "buy_stock")],
            goals=[Goal("maximize_profit")]
        )
        decision = self.reasoner.get_decision()
        logger.info(f"Market prediction decision: {decision}")
        return decision
    
    def report_results(self):
        # Report results to the user or contract (mock implementation)
        results = self.report_status()
        logger.info(f"Reporting results: {results}")

# Example usage (for illustration purposes, not part of the module)
if __name__ == "__main__":
    agent = FinancialAgent(id="financial_agent_001", owner="owner_001")
    agent.handle_lifecycle_event(AgentLifecycleEvent.INITIALIZE)
    agent.understand_agreement("buy low sell high")
    agent.request_market_data()
    agent.make_market_prediction()
    agent.report_results()

# Additional Financial Agent Examples

class AdvancedFinancialAgent(FinancialAgent):
    def __init__(self, id: str, owner: str):
        super().__init__(id, owner)
    
    def evaluate_risk(self, investment_data: str):
        # Evaluate investment risk based on provided data (mock implementation)
        logger.info(f"Evaluating risk for investment data: {investment_data}")
        risk_factors = investment_data.split()
        for factor in risk_factors:
            self.reasoner.kb.add_fact(Fact(f"risk_factor: {factor}"))
        risk_assessment = self.reasoner.get_decision()
        logger.info(f"Risk assessment: {risk_assessment}")
        return risk_assessment
    
    def diversify_portfolio(self):
        # Diversify portfolio (mock implementation)
        logger.info("Diversifying portfolio...")
        self.reasoner.update_knowledge(
            facts=[Fact("diversify = true")],
            rules=[Rule(["diversify = true"], "balance_assets")],
            goals=[Goal("minimize_risk")]
        )
        decision = self.reasoner.get_decision()
        logger.info(f"Portfolio diversification decision: {decision}")
        return decision

if __name__ == "__main__":
    advanced_agent = AdvancedFinancialAgent(id="advanced_financial_agent_001", owner="owner_002")
    advanced_agent.handle_lifecycle_event(AgentLifecycleEvent.INITIALIZE)
    advanced_agent.evaluate_risk("high volatility low liquidity")
    advanced_agent.diversify_portfolio()
    advanced_agent.request_market_data()
    advanced_agent.make_market_prediction()
    advanced_agent.report_results()