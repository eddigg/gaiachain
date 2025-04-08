# gaia-chain/frontend/cli/main.py

"""
GaiaChain CLI

This module serves as the entry point for the GaiaChain command-line interface (CLI).
It provides commands for deploying agents, deploying services, and monitoring agents within the GaiaChain ecosystem.

Usage:
    To deploy an agent:
        python main.py deploy-agent --agent-path <path> --contract-address <address> --stake-amount <amount> --web3-provider <provider>

    To deploy a service:
        python main.py deploy-service --service-path <path> --contract-address <address> --gaia-cost <cost> --web3-provider <provider>

    To monitor an agent:
        python main.py monitor-agent --agent-id <id> --contract-address <address> --web3-provider <provider> --log-path <path>

    To display the CLI version:
        python main.py version
"""

import argparse
import sys
from gaia_chain.tooling.deploy.deploy_agent import AgentDeployer
from gaia_chain.tooling.deploy.deploy_service import ServiceDeployer
from gaia_chain.tooling.monitoring.agent_monitor import AgentMonitor

def deploy_agent(args):
    """Deploy an agent using the deploy_agent.py module."""
    deployer = AgentDeployer(args.agent_path, args.contract_address, args.stake_amount, args.web3_provider)
    deployer.deploy()

def deploy_service(args):
    """Deploy a service using the deploy_service.py module."""
    deployer = ServiceDeployer(args.service_path, args.contract_address, args.gaia_cost, args.web3_provider)
    deployer.deploy()

def monitor_agent(args):
    """Monitor an agent using the agent_monitor.py module."""
    monitor = AgentMonitor(args.agent_id, args.contract_address, args.web3_provider, args.log_path)
    status = monitor.check_status()
    logs = monitor.view_logs()
    metrics = monitor.collect_metrics()
    print(f"Status: {status}")
    print(f"Logs:\n{logs}")
    print(f"Metrics: {metrics}")

def main():
    parser = argparse.ArgumentParser(description="GaiaChain CLI")
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="additional help")

    # Subcommand for deploying an agent
    parser_deploy_agent = subparsers.add_parser('deploy-agent', help="Deploy an agent")
    parser_deploy_agent.add_argument("--agent-path", required=True, help="Path to the agent code directory.")
    parser_deploy_agent.add_argument("--contract-address", required=True, help="Smart contract address for agent registration.")
    parser_deploy_agent.add_argument("--stake-amount", type=int, required=True, help="Amount of GAIA tokens to stake for agent registration.")
    parser_deploy_agent.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_deploy_agent.set_defaults(func=deploy_agent)

    # Subcommand for deploying a service
    parser_deploy_service = subparsers.add_parser('deploy-service', help="Deploy a service")
    parser_deploy_service.add_argument("--service-path", required=True, help="Path to the service code directory.")
    parser_deploy_service.add_argument("--contract-address", required=True, help="Smart contract address for service registration.")
    parser_deploy_service.add_argument("--gaia-cost", type=int, required=True, help="Cost of the service in GAIA tokens.")
    parser_deploy_service.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_deploy_service.set_defaults(func=deploy_service)

    # Subcommand for monitoring an agent
    parser_monitor_agent = subparsers.add_parser('monitor-agent', help="Monitor an agent")
    parser_monitor_agent.add_argument("--agent-id", required=True, help="ID of the agent to monitor.")
    parser_monitor_agent.add_argument("--contract-address", required=True, help="Smart contract address for agent status and metrics.")
    parser_monitor_agent.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_monitor_agent.add_argument("--log-path", required=True, help="Path to the directory containing agent logs.")
    parser_monitor_agent.set_defaults(func=monitor_agent)

    # Subcommand for displaying version
    parser_version = subparsers.add_parser('version', help="Display CLI version")
    parser_version.set_defaults(func=lambda args: print("GaiaChain CLI version 1.0"))

    # Parse arguments and call appropriate function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()