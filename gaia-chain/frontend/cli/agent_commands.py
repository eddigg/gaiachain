# gaia-chain/frontend/cli/agent_commands.py

"""
GaiaChain CLI - Agent Commands

This module provides command-line interface (CLI) commands for interacting with decentralized AI agents (dAls) in the GaiaChain ecosystem.
It includes commands to deploy agents, monitor their status, send instructions, and query their state.
"""

import argparse
from gaia_chain.tooling.deploy.deploy_agent import AgentDeployer
from gaia_chain.tooling.monitoring.agent_monitor import AgentMonitor

def deploy_agent(args):
    """Deploy an agent to the network."""
    deployer = AgentDeployer(args.agent_path, args.contract_address, args.stake_amount, args.web3_provider)
    deployer.deploy()

def monitor_agent(args):
    """Monitor an agent's status and performance."""
    monitor = AgentMonitor(args.agent_id, args.contract_address, args.web3_provider, args.log_path)
    status = monitor.check_status()
    logs = monitor.view_logs()
    metrics = monitor.collect_metrics()
    print(f"Status: {status}")
    print(f"Logs:\n{logs}")
    print(f"Metrics: {metrics}")

def send_instruction(args):
    """Send an instruction to a running agent."""
    # Assuming the agent runtime accepts DSL instructions via a file or API
    with open(args.dsl_file, 'r') as file:
        dsl_script = file.read()
    # Mock implementation: sending the instruction to the agent's runtime (e.g., writing to a file or API call)
    print(f"Sending instruction to agent {args.agent_id}:")
    print(dsl_script)
    # Here you would implement the actual sending logic, e.g., writing to a specific file or making an API call

def query_agent(args):
    """Query an agent's current state."""
    monitor = AgentMonitor(args.agent_id, args.contract_address, args.web3_provider, args.log_path)
    status = monitor.check_status()
    print(f"Current status of agent {args.agent_id}: {status}")

def main():
    parser = argparse.ArgumentParser(description="GaiaChain CLI - Agent Commands")
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="additional help")

    # Subcommand for deploying an agent
    parser_deploy_agent = subparsers.add_parser('deploy-agent', help="Deploy an agent")
    parser_deploy_agent.add_argument("--agent-path", required=True, help="Path to the agent code directory.")
    parser_deploy_agent.add_argument("--contract-address", required=True, help="Smart contract address for agent registration.")
    parser_deploy_agent.add_argument("--stake-amount", type=int, required=True, help="Amount of GAIA tokens to stake for agent registration.")
    parser_deploy_agent.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_deploy_agent.set_defaults(func=deploy_agent)

    # Subcommand for monitoring an agent
    parser_monitor_agent = subparsers.add_parser('monitor-agent', help="Monitor an agent")
    parser_monitor_agent.add_argument("--agent-id", required=True, help="ID of the agent to monitor.")
    parser_monitor_agent.add_argument("--contract-address", required=True, help="Smart contract address for agent status and metrics.")
    parser_monitor_agent.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_monitor_agent.add_argument("--log-path", required=True, help="Path to the directory containing agent logs.")
    parser_monitor_agent.set_defaults(func=monitor_agent)

    # Subcommand for sending instructions to an agent
    parser_send_instruction = subparsers.add_parser('send-instruction', help="Send an instruction to a running agent")
    parser_send_instruction.add_argument("--agent-id", required=True, help="ID of the agent to send the instruction to.")
    parser_send_instruction.add_argument("--dsl-file", required=True, help="Path to the DSL script file containing the instruction.")
    parser_send_instruction.set_defaults(func=send_instruction)

    # Subcommand for querying an agent's state
    parser_query_agent = subparsers.add_parser('query-agent', help="Query an agent's state")
    parser_query_agent.add_argument("--agent-id", required=True, help="ID of the agent to query.")
    parser_query_agent.add_argument("--contract-address", required=True, help="Smart contract address for agent status and metrics.")
    parser_query_agent.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_query_agent.add_argument("--log-path", required=True, help="Path to the directory containing agent logs.")
    parser_query_agent.set_defaults(func=query_agent)

    # Parse arguments and call appropriate function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()