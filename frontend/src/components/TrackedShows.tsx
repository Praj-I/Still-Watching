import { useState, useEffect } from 'react';
import { getTrackedShows, deleteShow, type Show } from '../api';
import './TrackedShows.css';

interface TrackedShowsProps {
    refreshTrigger: number;
}

function TrackedShows({refreshTrigger}: TrackedShowsProps) {
    const [shows, setShows] = useState<Show[]>([]);

    /* Load shows */
    async function loadShows() {
        try {
            const tracked = await getTrackedShows();
            setShows(tracked);
        } catch (error) {
        console.error(error);
        }
    }

    /* Get tracked shows */
    useEffect(() => {
        loadShows();
    }, [refreshTrigger]);

    /* Delete shows */
    async function handleDelete(netflixId: number) {
        try {
            await deleteShow(netflixId);
            setShows((prev) => prev.filter((s) => s.netflix_id !== netflixId));
        } catch (error) {
        console.error(error);
        }
    }

    if (shows.length === 0) {
        return <p className="empty-state">No shows tracked yet. Search above to add some.</p>;
    }

    /* Ticket UI */
    return (
        <div className="tracked-shows">
        {shows.map((show) => (
            <div className="ticket-stub" key={show.netflix_id}>
            <div className="ticket-main">
                <span className="ticket-label">Now tracking</span>
                <h3>{show.title}</h3>
            </div>
            <div className="ticket-perforation"></div>
            <div className="ticket-tear">
                <span className="bulb"></span>
                <button onClick={() => handleDelete(show.netflix_id)}>Remove</button>
            </div>
            </div>
        ))}
        </div>
    );
}

export default TrackedShows;