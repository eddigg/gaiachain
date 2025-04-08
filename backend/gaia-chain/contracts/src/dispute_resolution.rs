// gaia-chain/contracts/src/dispute_resolution.rs

// GaiaChain Dispute Resolution System
// This file implements the basic logic for a dispute resolution system within the GaiaChain ecosystem.
// It includes structures and functions for initiating, managing, and resolving disputes.

#![cfg_attr(not(feature = "std"), no_std)]

use ink_lang as ink;

#[ink::contract]
mod dispute_resolution {
    use ink_storage::collections::HashMap as StorageHashMap;
    use ink_prelude::vec::Vec;

    /// Dispute Status Enum
    #[derive(scale::Encode, scale::Decode, Clone, Debug, PartialEq, Eq)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub enum DisputeStatus {
        Pending,
        Voting,
        Resolved,
        Rejected,
    }

    /// Dispute Struct
    #[derive(scale::Encode, scale::Decode, Clone, Debug, PartialEq, Eq)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub struct Dispute {
        id: u64,
        initiator: AccountId,
        target: AccountId,
        reason: Vec<u8>,
        status: DisputeStatus,
        votes_for: u32,
        votes_against: u32,
        created_at: u64,
    }

    /// Dispute Resolution Contract
    #[ink(storage)]
    pub struct DisputeResolution {
        disputes: StorageHashMap<u64, Dispute>,
        dispute_count: u64,
    }

    impl DisputeResolution {
        /// Initializes the contract with no disputes.
        #[ink(constructor)]
        pub fn new() -> Self {
            Self {
                disputes: StorageHashMap::new(),
                dispute_count: 0,
            }
        }

        /// Initiates a new dispute.
        #[ink(message)]
        pub fn initiate_dispute(&mut self, target: AccountId, reason: Vec<u8>) -> Result<u64, String> {
            let initiator = self.env().caller();
            let dispute_id = self.dispute_count;
            let new_dispute = Dispute {
                id: dispute_id,
                initiator,
                target,
                reason,
                status: DisputeStatus::Pending,
                votes_for: 0,
                votes_against: 0,
                created_at: self.env().block_timestamp(),
            };
            self.disputes.insert(dispute_id, new_dispute);
            self.dispute_count += 1;
            Ok(dispute_id)
        }

        /// Updates the status of a dispute to Voting.
        #[ink(message)]
        pub fn start_voting(&mut self, dispute_id: u64) -> Result<(), String> {
            let caller = self.env().caller();
            let dispute = self.disputes.get_mut(&dispute_id).ok_or("Dispute not found")?;
            if dispute.initiator != caller {
                return Err("Only the initiator can start voting".to_string());
            }
            if dispute.status != DisputeStatus::Pending {
                return Err("Dispute is not in pending status".to_string());
            }
            dispute.status = DisputeStatus::Voting;
            Ok(())
        }

        /// Casts a vote on a dispute.
        #[ink(message)]
        pub fn vote(&mut self, dispute_id: u64, approve: bool) -> Result<(), String> {
            let dispute = self.disputes.get_mut(&dispute_id).ok_or("Dispute not found")?;
            if dispute.status != DisputeStatus::Voting {
                return Err("Dispute is not in voting status".to_string());
            }
            if approve {
                dispute.votes_for += 1;
            } else {
                dispute.votes_against += 1;
            }
            Ok(())
        }

        /// Resolves a dispute based on the votes.
        #[ink(message)]
        pub fn resolve_dispute(&mut self, dispute_id: u64) -> Result<(), String> {
            let dispute = self.disputes.get_mut(&dispute_id).ok_or("Dispute not found")?;
            if dispute.status != DisputeStatus::Voting {
                return Err("Dispute is not in voting status".to_string());
            }

            if dispute.votes_for > dispute.votes_against {
                dispute.status = DisputeStatus::Resolved;
                // Logic to handle successful dispute resolution (e.g., adjusting reputation, releasing funds)
            } else {
                dispute.status = DisputeStatus::Rejected;
                // Logic to handle rejected dispute (e.g., returning funds, penalizing the initiator)
            }
            Ok(())
        }

        /// Retrieves the details of a dispute by ID.
        #[ink(message)]
        pub fn get_dispute(&self, dispute_id: u64) -> Option<Dispute> {
            self.disputes.get(&dispute_id).cloned()
        }
    }
}