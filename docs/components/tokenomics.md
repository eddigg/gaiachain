🌐 GaiaChain Tokenomics (GAIA)
🎯 Purpose
The GAIA token is the lifeblood of GaiaChain’s decentralized intelligence economy. It facilitates value exchange, incentivizes contributions, and secures the network through staking and governance. This document outlines the GAIA token's function, utility, distribution, and flow across the system.

🪙 Token Overview
Property	Description
Token Name	GAIA
Type	Utility + Governance Token
Chain	Ethereum-compatible (EVM or L2 optimized)
Decimals	18
Supply	Fixed max supply (e.g., 1B GAIA)
🧬 Token Supply & Distribution
Allocation	Percentage	Purpose
Protocol Reserve	20%	Long-term sustainability and dev bounties
DAO Treasury	25%	Community-governed proposals and grants
Compute Providers	15%	Incentives for running decentralized infrastructure
Early Contributors	10%	Founders, researchers, and early validators
Agent Creators	15%	Bounties and rewards for agent development
Public Sale	10%	Token generation event
Liquidity Bootstrapping	5%	Initial DEX liquidity and staking pool formation
Vesting schedules and emission curves are DAO-configurable post-launch.

🔐 Staking & Governance
✅ Staking Mechanisms
Agent Onboarding: Developers must stake GAIA to submit new dAIs for evaluation. Slashing applies for bad actors or broken models.

Validator Staking: Compute nodes stake GAIA to participate in decentralized inference tasks.

User Delegation: Token holders may delegate stake to specific swarms, compute clusters, or governance reps.

🗳️ Governance Participation
GAIA holders vote on:

Protocol upgrades

Agent lifecycle decisions (onboarding, pruning)

Treasury allocation

Ecosystem parameters (e.g., gas fees, inflation)

Reputation-weighted voting may complement raw token stake using agent contribution proofs.

💸 Payments and Service Access
User Actions Requiring GAIA:
Action	Payment Type
AI service requests (inference)	Per-request fee
Agent training bounties	GAIA bounty
Data contributions	Usage rewards
Premium licensing for agents	Subscription or token stream
Payments are routed via smart contracts.

Pricing is algorithmic (supply-demand curves, DAO votes, or bonding curves).

🔁 Token Flow Between Actors
mermaid
Copy
Edit
flowchart LR
    User([User])
    dAI([AI Agent])
    DAO([DAO Treasury])
    Node([Compute Node])
    Dev([Agent Developer])
    Data([Data Provider])

    User -->|GAIA Payment| dAI
    dAI -->|% Fee| Node
    dAI -->|% Fee| Dev
    Dev -->|Stake| DAO
    Node -->|Proof of Compute| DAO
    Data -->|Data Licensing| dAI
    DAO -->|Reward| Data
dAIs receive GAIA for task execution.

Developers earn GAIA when their agents are used or licensed.

Compute Nodes are rewarded based on throughput and SLA adherence.

Data Providers are compensated for clean, privacy-preserving datasets.

🎯 Incentive Summary
Role	How GAIA Is Earned
Agent Developers	Through usage-based rewards and bounties
Users	N/A (GAIA is spent to access services)
Validators	Compute contributions
Data Providers	Privacy-safe contributions to training
Governance Participants	Proposal approval and DAO voting rewards
🧭 Future Tokenomics Considerations
Dynamic Emissions: DAO-governed adaptive inflation tied to network growth.

Reputation Score Staking Boosts: High-performing actors earn compounding rewards.

Cross-Chain Utility: Wrapped GAIA on L2s or Cosmos IBC for faster/cheaper usage.

Agent-specific Token Curves: Microeconomies for individual agents or swarms.

