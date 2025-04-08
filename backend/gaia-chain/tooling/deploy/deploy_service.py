# gaia-chain/tooling/deploy/deploy_service.py

"""
Deploy Service to GaiaChain

This module defines the logic to package and deploy services within the GaiaChain ecosystem.
It includes steps for packaging the service, registering it with smart contracts, and optionally setting up its runtime environment.
"""

import os
import tarfile
import json
import logging
import subprocess
from web3 import Web3
from argparse import ArgumentParser

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceDeployer:
    def __init__(self, service_path, contract_address, gaia_cost, web3_provider):
        self.service_path = service_path
        self.contract_address = contract_address
        self.gaia_cost = gaia_cost
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract = None  # Placeholder for smart contract instance

    def package_service(self):
        """Package the service for deployment."""
        logger.info("Packaging service...")
        tar_path = f"{self.service_path}.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(self.service_path, arcname=os.path.basename(self.service_path))
        logger.info(f"Service packaged at {tar_path}")
        return tar_path

    def register_service(self):
        """Register the service with the smart contract."""
        logger.info("Registering service with the smart contract...")
        # Load contract ABI and bytecode (assumed to be available in the service path)
        with open(os.path.join(self.service_path, 'contract_abi.json'), 'r') as abi_file:
            contract_abi = json.load(abi_file)
        with open(os.path.join(self.service_path, 'contract_bytecode.bin'), 'r') as bytecode_file:
            contract_bytecode = bytecode_file.read()

        # Initialize the contract instance
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=contract_abi, bytecode=contract_bytecode)

        # Register the service (mock implementation, replace with actual registration logic)
        tx_hash = self.contract.functions.registerService(self.web3.eth.defaultAccount, self.gaia_cost).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        logger.info(f"Service registered with transaction hash: {tx_hash.hex()}")

    def setup_runtime(self):
        """Set up the service's runtime environment."""
        logger.info("Setting up runtime environment...")
        # Install dependencies (mock implementation)
        subprocess.run(["pip", "install", "-r", os.path.join(self.service_path, "requirements.txt")], check=True)
        logger.info("Dependencies installed.")
        
        # Start the service runtime (mock implementation)
        subprocess.run(["python", os.path.join(self.service_path, "service_core.py")], check=True)
        logger.info("Service runtime started.")

    def deploy(self):
        """Deploy the service to GaiaChain."""
        self.package_service()
        self.register_service()
        self.setup_runtime()
        logger.info("Service deployed successfully.")

if __name__ == "__main__":
    parser = ArgumentParser(description="Deploy a service to GaiaChain.")
    parser.add_argument("--service-path", required=True, help="Path to the service code directory.")
    parser.add_argument("--contract-address", required=True, help="Smart contract address for service registration.")
    parser.add_argument("--gaia-cost", type=int, required=True, help="Cost of the service in GAIA tokens.")
    parser.add_argument("--web3-provider", default="http://localhost:8545", help="Web3 provider URL.")
    
    args = parser.parse_args()

    deployer = ServiceDeployer(args.service_path, args.contract_address, args.gaia_cost, args.web3_provider)
    deployer.deploy()