import { useState } from 'react';
import type { Show } from '../api';
import './SelectedShowsPopup.css';

interface SelectedShowsPopupProps {
    shows: Show[];
    needsEmail: boolean;
    onSave: (email?: string) => void;
    onClose: () => void;
}

function SelectedShowsPopup({ shows, needsEmail, onSave, onClose }: SelectedShowsPopupProps) {
    const [email, setEmail] = useState('');

    /* If user is first-time user */
    function handleSaveClick() {
        if (needsEmail) {
            onSave(email);
        } else {
            onSave();
        }
    }

    return (
        <div className="popup-overlay">
            <div className="popup">
                <h2>Selected shows</h2>
                <ul>
                {shows.map((show) => (
                    <li key={show.netflix_id}>{show.title}</li>
                ))}
                </ul>

                {needsEmail && (
                <div className="email-field">
                    <label htmlFor="notify-email">Notification email</label>
                    <input
                        id="notify-email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="you@example.com"
                    />
                </div>
                )}

                <div className="popup-actions">
                <button onClick={onClose}>Cancel</button>
                <button
                    className="save-button"
                    onClick={handleSaveClick}
                    disabled={needsEmail && !email.trim()}
                >
                    Save
                </button>
                </div>
            </div>
        </div>
    );
}

export default SelectedShowsPopup;