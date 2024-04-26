import hashlib
import random
import matplotlib.pyplot as plt
import numpy as np

# Define the Candidate class to represent candidates
class Candidate:
    def __init__(self, name, party, campaign_quote):
        self.name = name
        self.party = party
        self.campaign_quote = campaign_quote

    def __str__(self):
        return f"{self.name} ({self.party}): {self.campaign_quote}"

# Define the Voter class to represent voters
class Voter:
    def __init__(self, name):
        self.name = name
        self.voter_id = self.generate_voter_id(name)
        self.has_voted = False

    def __str__(self):
        return f"{self.name} (Voter ID: {self.voter_id})"

    # Generate a unique voter ID using SHA-256 hashing
    def generate_voter_id(self, name):
        return hashlib.sha256(name.encode()).hexdigest()[:8]

# Define the Ballot class to represent individual votes
class Ballot:
    def __init__(self, voter_id, encrypted_vote):
        self.voter_id = voter_id
        self.encrypted_vote = encrypted_vote

    def __str__(self):
        return f"Voter ID: {self.voter_id}, Encrypted Vote: {self.encrypted_vote}"

# Define the Election class to manage the entire electoral process
class Election:
    def __init__(self, parties):
        self.parties = parties
        self.voters = {}
        self.ballots = []

    # Register a new voter
    def register_voter(self, voter):
        if voter.voter_id not in self.voters:
            self.voters[voter.voter_id] = voter
            print(f"Voter {voter.name} registered successfully.")
        else:
            print("Voter already registered.")

    # Authenticate a voter before allowing them to vote
    def authenticate_voter(self, voter_id):
        return voter_id in self.voters and not self.voters[voter_id].has_voted

    # Simulate encryption of vote
    def encrypt_vote(self, voter_id, candidate):
        # Simulate encryption (e.g., using a random key)
        key = random.randint(1, 1000)
        encrypted_vote = f"{voter_id}-{candidate.name}-{key}"
        return encrypted_vote

    # Allow a voter to cast their vote
    def vote(self, voter_id, candidate):
        if self.authenticate_voter(voter_id):
            encrypted_vote = self.encrypt_vote(voter_id, candidate)
            self.ballots.append(Ballot(voter_id, encrypted_vote))
            self.voters[voter_id].has_voted = True
            print(f"Vote cast successfully for {candidate.name}.")
        else:
            print("Voter not authenticated or already voted.")

    # Decrypt the encrypted vote
    def decrypt_vote(self, encrypted_vote):
        try:
            parts = encrypted_vote.split("-")
            if len(parts) == 3:
                voter_id, candidate_name, _ = parts
                return voter_id, candidate_name
            else:
                raise ValueError("Incorrect format of encrypted vote")
        except ValueError as e:
            print(f"Error: {e}")
            return None, None

    # Count votes and visualize results
    def count_votes(self):
        print("Vote Count:")
        party_results = {party[0].party: {candidate: 0 for candidate in party} for party in self.parties}
        for ballot in self.ballots:
            voter_id, candidate_name = self.decrypt_vote(ballot.encrypted_vote)
            if voter_id is not None and candidate_name is not None:
                candidate = None
                for party in self.parties:
                    candidate = next((c for c in party if c.name == candidate_name), None)
                    if candidate:
                        break
                if candidate:
                    party_results[candidate.party][candidate] += 1

        # Print vote counts for each party
        for party, results in party_results.items():
            print(f"\n{party} Vote Count:")
            for candidate, votes in results.items():
                print(f"{candidate.name}: {votes} votes")

        # Visualize results using a bar graph
        num_parties = len(self.parties)
        num_candidates = max(len(party) for party in self.parties)
        fig, ax = plt.subplots()
        index = np.arange(num_candidates)
        bar_width = 0.2
        opacity = 0.8

        for i, party in enumerate(self.parties):
            candidates = [candidate.name for candidate in party]
            votes = [party_results[party[0].party][candidate] for candidate in party]
            ax.bar(index + i * bar_width, votes, bar_width, alpha=opacity, label=party[0].party)

        ax.set_xlabel('Candidates')
        ax.set_ylabel('Number of Votes')
        ax.set_title('Election Results by Party')
        ax.set_xticks(index + bar_width * (num_parties - 1) / 2)
        ax.set_xticklabels(candidates)
        ax.legend()

        plt.tight_layout()
        plt.show()

# Define the main function
def main():
    # Define parties with their candidates and campaign quotes
    party1_candidates = [
        Candidate("Candidate A", "Party X", "Vote for progress!"),
        Candidate("Candidate B", "Party X", "Together for a brighter future!")
    ]

    party2_candidates = [
        Candidate("Candidate C", "Party Y", "For a fair and just society!"),
        Candidate("Candidate D", "Party Y", "Building a better tomorrow!")
    ]

    party3_candidates = [
        Candidate("Candidate E", "Party Z", "Innovate for a sustainable future!"),
        Candidate("Candidate F", "Party Z", "Empowering communities, together!")
    ]

    # Initialize election with parties
    election = Election([
        party1_candidates,
        party2_candidates,
        party3_candidates
    ])

    # Register voters
    voters = [Voter(f"Voter{i}") for i in range(1, 31)]
    for voter in voters:
        election.register_voter(voter)

    # Simulate voting process
    for voter in voters:
        party = random.choice(election.parties)
        candidate = random.choice(party)
        election.vote(voter.voter_id, candidate)

    # Count votes and visualize results
    election.count_votes()

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
