# gaia-chain/frontend/cli/service_commands.py

"""
GaiaChain CLI - Service Commands

This module provides command-line interface (CLI) commands for interacting with services in the GaiaChain ecosystem.
It includes commands to deploy services, monitor their status and usage, and interact with them by sending requests.
"""

import argparse
from gaia_chain.tooling.deploy.deploy_service import ServiceDeployer
from web3 import Web3

def deploy_service(args):
    """Deploy a service to the network."""
    deployer = ServiceDeployer(args.service_path, args.contract_address, args.gaia_cost, args.web3_provider)
    deployer.deploy()

def monitor_service(args):
    """Monitor a service's status or usage."""
    web3 = Web3(Web3.HTTPProvider(args.web3_provider))
    contract = web3.eth.contract(address=args.contract_address, abi=args.contract_abi)
    
    # Query service status from smart contract (mock implementation)
    status = contract.functions.getServiceStatus(args.service_id).call()
    usage_stats = contract.functions.getServiceUsageStats(args.service_id).call()
    
    print(f"Service {args.service_id} status: {status}")
    print(f"Service {args.service_id} usage stats: {usage_stats}")

def request_service(args):
    """Send a request to a deployed service."""
    web3 = Web3(Web3.HTTPProvider(args.web3_provider))
    contract = web3.eth.contract(address=args.contract_address, abi=args.contract_abi)
    
    # Read DSL request from file
    with open(args.dsl_file, 'r') as file:
        dsl_request = file.read()
    
    # Send service request (mock implementation)
    tx_hash = contract.functions.requestService(args.service_id, dsl_request, args.payment_amount).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    
    print(f"Service request sent with transaction hash: {tx_hash.hex()}")

def main():
    parser = argparse.ArgumentParser(description="GaiaChain CLI - Service Commands")
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands", help="additional help")

    # Subcommand for deploying a service
    parser_deploy_service = subparsers.add_parser('deploy-service', help="Deploy a service")
    parser_deploy_service.add_argument("--service-path", required=True, help="Path to the service code directory.")
    parser_deploy_service.add_argument("--contract-address", required=True, help="Smart contract address for service registration.")
    parser_deploy_service.add_argument("--gaia-cost", type=int, required=True, help="Cost of the service in GAIA tokens.")
    parser_deploy_service.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_deploy_service.set_defaults(func=deploy_service)

    # Subcommand for monitoring a service
    parser_monitor_service = subparsers.add_parser('monitor-service', help="Monitor a service")
    parser_monitor_service.add_argument("--service-id", required=True, help="ID of the service to monitor.")
    parser_monitor_service.add_argument("--contract-address", required=True, help="Smart contract address for service status and metrics.")
    parser_monitor_service.add_argument("--contract-abi", required=True, help="Path to the contract ABI JSON file.")
    parser_monitor_service.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_monitor_service.set_defaults(func=monitor_service)

    # Subcommand for sending requests to a service
    parser_request_service = subparsers.add_parser('request-service', help="Send a request to a deployed service")
    parser_request_service.add_argument("--service-id", required=True, help="ID of the service to request.")
    parser_request_service.add_argument("--dsl-file", required=True, help="Path to the DSL script file containing the request.")
    parser_request_service.add_argument("--payment-amount", type=int, required=True, help="Amount of GAIA tokens to pay for the service request.")
    parser_request_service.add_argument("--contract-address", required=True, help="Smart contract address for service interaction.")
    parser_request_service.add_argument("--contract-abi", required=True, help="Path to the contract ABI JSON file.")
    parser_request_service.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    parser_request_service.set_defaults(func=request_service)

    # Parse arguments and call appropriate function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()