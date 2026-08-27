import { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import SelectedShowsPopup from './components/SelectedShowsPopup';
import TrackedShows from './components/TrackedShows';
import { getNotificationEmail, initialSetup, addShows, type Show } from './api';
import "./App.css"

function App() {
  const [selectedShows, setSelectedShows] = useState<Show[]>([]);
  const [existingEmail, setExistingEmail] = useState<string | null>(null);
  const [showPopup, setShowPopup] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  /* Check if a notification email is already set */
  useEffect(() => {
    getNotificationEmail()
      .then(setExistingEmail)
      .catch((err) => console.error(err));
  }, []);

  /* Checklist toggle */
  function toggleShow(chosen_show: Show) {
    setSelectedShows((prev) => {
      const alreadySelected = prev.some((possible_show) => possible_show.netflix_id === chosen_show.netflix_id);

      /* Remove if already selected */
      if (alreadySelected) {
        return prev.filter((possible_show) => possible_show.netflix_id !== chosen_show.netflix_id);
      }

      /* Add if not selected */
      return [...prev, chosen_show];
    });
  }

  /* Save selected shows, both for first-time and returning users */
  async function handleSave(email?: string) {
    try {
      if (existingEmail) {
        await addShows(selectedShows);
      } else if (email) {
        await initialSetup(selectedShows, email);
        setExistingEmail(email);
      }
      setStatusMessage(`${selectedShows.length} show(s) saved.`);
      setSelectedShows([]);
      setShowPopup(false);
      setRefreshTrigger((prev) => prev + 1);
      setTimeout(() => setStatusMessage(null), 3000);
    } catch (error) {
      console.error(error);
      setStatusMessage('Something went wrong. Please try again.');
    }
  }

  return (
    <div className="app-shell">
      <h1 className="app-title">Still Watching</h1>
      {statusMessage && <div className="status-message">{statusMessage}</div>}

      <SearchBar selectedShows={selectedShows} onToggleShow={toggleShow} />

      {selectedShows.length > 0 && (
        <button className="review-button" onClick={() => setShowPopup(true)}>
          Review {selectedShows.length} selected show{selectedShows.length > 1 ? 's' : ''}
        </button>
      )}

      {showPopup && (
        <SelectedShowsPopup
          shows={selectedShows}
          needsEmail={!existingEmail}
          onSave={handleSave}
          onClose={() => setShowPopup(false)}
        />
      )}

      <TrackedShows refreshTrigger={refreshTrigger} />
    </div>
  );
}

export default App;
