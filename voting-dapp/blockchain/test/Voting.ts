import { expect } from "chai";
import { network } from "hardhat";

// Buat network connection (top-level await di Hardhat 3)
const { ethers, networkHelpers } = await network.create();

describe("Voting Contract", function () {
  // Fixture untuk deploy contract (di-cache oleh loadFixture)
  async function deployVotingFixture() {
    const [owner, voter1, voter2] = await ethers.getSigners();
    const voting = await ethers.deployContract("Voting");
    return { voting, owner, voter1, voter2 };
  }

  describe("Deployment", function () {
    it("Harus set owner dengan benar", async function () {
      const { voting, owner } = await networkHelpers.loadFixture(deployVotingFixture);
      const contractOwner = await voting.owner();
      expect(contractOwner).to.equal(owner.address);
    });

    it("Voting harus tertutup di awal", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      const isOpen = await voting.votingOpen();
      expect(isOpen).to.equal(false);
    });

    it("Jumlah kandidat awal harus 0", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      const count = await voting.candidatesCount();
      expect(count).to.equal(0n);
    });
  });

  describe("Add Candidate", function () {
    it("Owner bisa menambah kandidat", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      await voting.addCandidate("Kandidat A");

      const candidate = await voting.candidates(1);
      expect(candidate.name).to.equal("Kandidat A");
      expect(candidate.voteCount).to.equal(0n);
    });

    it("Non-owner tidak bisa menambah kandidat", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployVotingFixture);
      await expect(
        voting.connect(voter1).addCandidate("Kandidat B")
      ).to.be.revertedWith("Hanya owner yang bisa melakukan ini");
    });

    it("Nama kandidat tidak boleh kosong", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      await expect(
        voting.addCandidate("")
      ).to.be.revertedWith("Nama tidak boleh kosong");
    });
  });

  describe("Voting", function () {
    // Fixture dengan kandidat sudah ditambahkan
    async function deployWithCandidatesFixture() {
      const { voting, owner, voter1, voter2 } = await deployVotingFixture();
      await voting.addCandidate("Kandidat A");
      await voting.addCandidate("Kandidat B");
      await voting.setVotingStatus(true);
      return { voting, owner, voter1, voter2 };
    }

    it("Voter bisa melakukan voting", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await voting.connect(voter1).vote(1);

      const candidate = await voting.candidates(1);
      expect(candidate.voteCount).to.equal(1n);

      const hasVoted = await voting.hasVoted(voter1.address);
      expect(hasVoted).to.equal(true);
    });

    it("Voter tidak bisa vote 2 kali", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await voting.connect(voter1).vote(1);

      await expect(
        voting.connect(voter1).vote(2)
      ).to.be.revertedWith("Anda sudah melakukan voting");
    });

    it("Tidak bisa vote jika voting ditutup", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await voting.setVotingStatus(false);

      await expect(
        voting.connect(voter1).vote(1)
      ).to.be.revertedWith("Voting belum dibuka atau sudah ditutup");
    });

    it("Tidak bisa vote kandidat yang tidak ada", async function () {
      const { voting, voter1 } = await networkHelpers.loadFixture(deployWithCandidatesFixture);
      await expect(
        voting.connect(voter1).vote(99)
      ).to.be.revertedWith("Kandidat tidak valid");
    });
  });

  describe("Get Candidates", function () {
    it("Harus mengembalikan semua kandidat", async function () {
      const { voting } = await networkHelpers.loadFixture(deployVotingFixture);
      await voting.addCandidate("Kandidat A");
      await voting.addCandidate("Kandidat B");
      await voting.addCandidate("Kandidat C");

      const candidates = await voting.getAllCandidates();
      expect(candidates.length).to.equal(3);
      expect(candidates[0].name).to.equal("Kandidat A");
      expect(candidates[1].name).to.equal("Kandidat B");
      expect(candidates[2].name).to.equal("Kandidat C");
    });
  });

  describe("Total Votes", function () {
    it("Harus menghitung total votes dengan benar", async function () {
      const { voting, voter1, voter2 } = await networkHelpers.loadFixture(deployVotingFixture);
      await voting.addCandidate("Kandidat A");
      await voting.addCandidate("Kandidat B");
      await voting.setVotingStatus(true);

      await voting.connect(voter1).vote(1);
      await voting.connect(voter2).vote(2);

      const totalVotes = await voting.getTotalVotes();
      expect(totalVotes).to.equal(2n);
    });
  });
});
