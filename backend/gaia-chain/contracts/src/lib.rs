// gaia-chain/contracts/src/lib.rs

// GaiaChain Smart Contract
// This file defines the main smart contract logic for the GaiaChain ecosystem.
// It includes GAIA token management (minting, transfer, burning), staking/unstaking,
// agent registration (with verification), service interactions, and rewards distribution.

#![cfg_attr(not(feature = "std"), no_std)]

use ink_lang as ink;

#[ink::contract]
mod gaiachain {
    use ink_storage::collections::HashMap as StorageHashMap;

    /// GAIA Token Management and Agent Registry
    #[ink(storage)]
    pub struct GaiaChain {
        owner: AccountId,                              // Contract owner who can mint tokens.
        total_supply: Balance,                         // Total supply of GAIA tokens.
        balances: StorageHashMap<AccountId, Balance>,  // Mapping of account balances.
        stakes: StorageHashMap<AccountId, Balance>,    // Mapping of staked tokens per account.
        agent_registry: StorageHashMap<AccountId, Agent>, // Registered agents.
    }

    #[derive(scale::Encode, scale::Decode, Clone, Debug, PartialEq, Eq)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub struct Agent {
        id: AccountId,        // Unique identifier for the agent.
        owner: AccountId,     // The account that owns the agent.
        stake: Balance,       // The amount of GAIA tokens staked by the agent.
        reputation: u32,      // The starting reputation of the agent (initialized to 0).
    }

    impl GaiaChain {
        /// Initializes the contract with a fixed total supply of GAIA tokens and sets the caller as the owner.
        #[ink(constructor)]
        pub fn new(initial_supply: Balance) -> Self {
            let caller = Self::env().caller();
            let mut balances = StorageHashMap::new();
            balances.insert(caller, initial_supply);

            Self {
                owner: caller,
                total_supply: initial_supply,
                balances,
                stakes: StorageHashMap::new(),
                agent_registry: StorageHashMap::new(),
            }
        }

        /// Mints new GAIA tokens to the specified account.
        /// Only the contract owner can call this function.
        #[ink(message)]
        pub fn mint(&mut self, to: AccountId, amount: Balance) -> Result<(), String> {
            let caller = self.env().caller();
            if caller != self.owner {
                return Err("Only the contract owner can mint tokens".to_string());
            }
            let to_balance = self.balances.get(&to).copied().unwrap_or(0);
            self.balances.insert(to, to_balance + amount);
            self.total_supply += amount;
            Ok(())
        }

        /// Burns (destroys) GAIA tokens from the caller's account.
        #[ink(message)]
        pub fn burn(&mut self, amount: Balance) -> Result<(), String> {
            let caller = self.env().caller();
            let caller_balance = self.balances.get(&caller).copied().unwrap_or(0);
            if caller_balance < amount {
                return Err("Insufficient balance to burn".to_string());
            }
            self.balances.insert(caller, caller_balance - amount);
            self.total_supply -= amount;
            Ok(())
        }

        /// Transfers GAIA tokens from the caller's account to another account.
        #[ink(message)]
        pub fn transfer(&mut self, to: AccountId, amount: Balance) -> Result<(), String> {
            let from = self.env().caller();
            let from_balance = self.balances.get(&from).copied().unwrap_or(0);
            if from_balance < amount {
                return Err("Insufficient balance".to_string());
            }
            self.balances.insert(from, from_balance - amount);
            let to_balance = self.balances.get(&to).copied().unwrap_or(0);
            self.balances.insert(to, to_balance + amount);
            Ok(())
        }

        /// Stakes GAIA tokens for agent registration or other purposes.
        #[ink(message)]
        pub fn stake(&mut self, amount: Balance) -> Result<(), String> {
            let caller = self.env().caller();
            let caller_balance = self.balances.get(&caller).copied().unwrap_or(0);
            if caller_balance < amount {
                return Err("Insufficient balance".to_string());
            }
            self.balances.insert(caller, caller_balance - amount);
            let caller_stake = self.stakes.get(&caller).copied().unwrap_or(0);
            self.stakes.insert(caller, caller_stake + amount);
            Ok(())
        }

        /// Unstakes GAIA tokens, returning them to the caller's available balance.
        #[ink(message)]
        pub fn unstake(&mut self, amount: Balance) -> Result<(), String> {
            let caller = self.env().caller();
            let caller_stake = self.stakes.get(&caller).copied().unwrap_or(0);
            if caller_stake < amount {
                return Err("Insufficient staked balance".to_string());
            }
            self.stakes.insert(caller, caller_stake - amount);
            let caller_balance = self.balances.get(&caller).copied().unwrap_or(0);
            self.balances.insert(caller, caller_balance + amount);
            Ok(())
        }

        /// Registers a new agent on the GaiaChain.
        ///
        /// Registration Details:
        /// - **Agent ID (id):** Unique identifier for the agent.
        /// - **Owner (owner):** The account registering the agent.
        /// - **Stake (stake):** The amount of GAIA tokens staked by the agent.
        /// - **Reputation (reputation):** Initialized to 0 upon registration.
        ///
        /// The function checks if the owner has sufficient staked balance.
        /// If the check passes, a new Agent struct is created and stored on-chain in the agent_registry.
        #[ink(message)]
        pub fn register_agent(&mut self, id: AccountId, stake: Balance) -> Result<(), String> {
            let owner = self.env().caller();
            // Verification: Ensure the caller has enough staked balance.
            if self.stakes.get(&owner).copied().unwrap_or(0) < stake {
                return Err("Insufficient staked balance".to_string());
            }
            let agent = Agent {
                id,
                owner,
                stake,
                reputation: 0,
            };
            self.agent_registry.insert(id, agent);
            Ok(())
        }

        /// Requests a service from an agent with a specified payment and constraints.
        #[ink(message)]
        pub fn request_service(&mut self, agent_id: AccountId, payment: Balance, constraints: Vec<String>) -> Result<(), String> {
            let requester = self.env().caller();
            let requester_balance = self.balances.get(&requester).copied().unwrap_or(0);
            if requester_balance < payment {
                return Err("Insufficient balance".to_string());
            }
            self.balances.insert(requester, requester_balance - payment);
            let agent_balance = self.balances.get(&agent_id).copied().unwrap_or(0);
            self.balances.insert(agent_id, agent_balance + payment);
            // Additional logic for handling service request and constraints can be added here.
            Ok(())
        }

        /// Records the completion of a service task, releasing funds to the agent.
        #[ink(message)]
        pub fn complete_service(&mut self, agent_id: AccountId, success: bool) -> Result<(), String> {
            if success {
                // Logic for successful service completion can be added here.
                Ok(())
            } else {
                // Logic for handling failure or disputes can be added here.
                Err("Service completion failed".to_string())
            }
        }

        /// Distributes rewards to users based on predefined criteria.
        #[ink(message)]
        pub fn distribute_rewards(&mut self, recipients: Vec<(AccountId, Balance)>) -> Result<(), String> {
            for (account, reward) in recipients {
                let balance = self.balances.get(&account).copied().unwrap_or(0);
                self.balances.insert(account, balance + reward);
            }
            Ok(())
        }
    }
}
