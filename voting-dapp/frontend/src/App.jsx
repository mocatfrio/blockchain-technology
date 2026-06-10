import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { CONTRACT_ADDRESS, CONTRACT_ABI } from './config/contract';
import './App.css';

function App() {
  const [account, setAccount] = useState(null);
  const [contract, setContract] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [hasVoted, setHasVoted] = useState(false);
  const [votingOpen, setVotingOpen] = useState(false);
  const [isOwner, setIsOwner] = useState(false);
  const [loading, setLoading] = useState(false);
  const [totalVotes, setTotalVotes] = useState(0);

  // Connect ke MetaMask
  const connectWallet = async () => {
    try {
      if (!window.ethereum) {
        alert('MetaMask tidak terdeteksi! Silakan install MetaMask.');
        return;
      }

      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      });

      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const votingContract = new ethers.Contract(
        CONTRACT_ADDRESS,
        CONTRACT_ABI,
        signer
      );

      setAccount(accounts[0]);
      setContract(votingContract);

      // Cek apakah user adalah owner
      const owner = await votingContract.owner();
      setIsOwner(owner.toLowerCase() === accounts[0].toLowerCase());

    } catch (error) {
      console.error('Error connecting wallet:', error);
    }
  };

  // Load data dari contract
  const loadContractData = async () => {
    if (!contract || !account) return;

    try {
      setLoading(true);

      // Get semua kandidat
      const allCandidates = await contract.getAllCandidates();
      const formattedCandidates = allCandidates.map(c => ({
        id: Number(c.id),
        name: c.name,
        voteCount: Number(c.voteCount)
      }));
      setCandidates(formattedCandidates);

      // Cek status voting
      const isOpen = await contract.votingOpen();
      setVotingOpen(isOpen);

      // Cek apakah user sudah vote
      const voted = await contract.checkIfVoted(account);
      setHasVoted(voted);

      // Get total votes
      const total = await contract.getTotalVotes();
      setTotalVotes(Number(total));

    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Vote untuk kandidat
  const voteForCandidate = async (candidateId) => {
    if (!contract) return;

    try {
      setLoading(true);
      const tx = await contract.vote(candidateId);
      await tx.wait();

      alert('Vote berhasil!');
      await loadContractData();
    } catch (error) {
      console.error('Error voting:', error);
      alert('Gagal vote: ' + (error.reason || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Toggle status voting (owner only)
  const toggleVoting = async () => {
    if (!contract) return;

    try {
      setLoading(true);
      const tx = await contract.setVotingStatus(!votingOpen);
      await tx.wait();

      await loadContractData();
    } catch (error) {
      console.error('Error toggling voting:', error);
      alert('Gagal mengubah status voting');
    } finally {
      setLoading(false);
    }
  };

  // Load data ketika contract atau account berubah
  useEffect(() => {
    if (contract && account) {
      loadContractData();
    }
  }, [contract, account]);

  // Listen untuk perubahan account
  useEffect(() => {
    if (window.ethereum) {
      window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length > 0) {
          setAccount(accounts[0]);
        } else {
          setAccount(null);
          setContract(null);
        }
      });
    }
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Voting dApp</h1>
        <p>Sistem Voting Berbasis Blockchain</p>
      </header>

      <main>
        {!account ? (
          <div className="connect-section">
            <p>Silakan connect wallet untuk mulai voting</p>
            <button onClick={connectWallet} className="btn-primary">
              Connect MetaMask
            </button>
          </div>
        ) : (
          <div className="voting-section">
            <div className="info-box">
              <p><strong>Connected:</strong> {account.slice(0, 6)}...{account.slice(-4)}</p>
              <p><strong>Status Voting:</strong> {votingOpen ? '🟢 Dibuka' : '🔴 Ditutup'}</p>
              <p><strong>Total Votes:</strong> {totalVotes}</p>
              {hasVoted && <p className="voted-badge">Anda sudah melakukan voting</p>}
            </div>

            {isOwner && (
              <div className="admin-panel">
                <h3>Admin Panel</h3>
                <button
                  onClick={toggleVoting}
                  disabled={loading}
                  className={votingOpen ? 'btn-danger' : 'btn-success'}
                >
                  {votingOpen ? 'Tutup Voting' : 'Buka Voting'}
                </button>
              </div>
            )}

            <h2>Daftar Kandidat</h2>

            {loading ? (
              <p>Loading...</p>
            ) : (
              <div className="candidates-grid">
                {candidates.map((candidate) => (
                  <div key={candidate.id} className="candidate-card">
                    <h3>{candidate.name}</h3>
                    <p className="vote-count">{candidate.voteCount} votes</p>
                    <div className="progress-bar">
                      <div
                        className="progress"
                        style={{
                          width: totalVotes > 0
                            ? `${(candidate.voteCount / totalVotes) * 100}%`
                            : '0%'
                        }}
                      />
                    </div>
                    <button
                      onClick={() => voteForCandidate(candidate.id)}
                      disabled={hasVoted || !votingOpen || loading}
                      className="btn-vote"
                    >
                      {hasVoted ? 'Sudah Vote' : 'Vote'}
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      <footer>
        <p>Final Project - Teknologi Blockchain</p>
      </footer>
    </div>
  );
}

export default App;
