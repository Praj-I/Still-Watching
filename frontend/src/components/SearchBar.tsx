import { useState } from 'react';
import { searchShows, type Show } from '../api';
import "./SearchBar.css"

interface SearchBarProps {
    selectedShows: Show[];
    onToggleShow: (show: Show) => void;
}

/* Ensures results are most-relevant to least-relevant */
function filterRelevantResults(results: Show[], query: string): Show[] {
    const lowerQuery = query.toLowerCase().trim();

    return results.filter((show) =>
        show.title.toLowerCase().includes(lowerQuery)
    ).sort((a, b) => {
        const aTitle = a.title.toLowerCase();
        const bTitle = b.title.toLowerCase();

        if (aTitle === lowerQuery)
            return -1;
        if (bTitle === lowerQuery)
            return 1;

        const aStarts = aTitle.startsWith(lowerQuery);
        const bStarts = bTitle.startsWith(lowerQuery);

        if (aStarts && !bStarts)
            return -1;
        if (bStarts && !aStarts)
            return 1;

        return 0;
    });
}

function SearchBar({ selectedShows, onToggleShow }: SearchBarProps) {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Show[]>([]);
    const [loading, setLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);

    async function handleSearch(event: React.SubmitEvent<HTMLFormElement>) {
        /*Prevent browser reload*/
        event.preventDefault();

        /*Avoid API calls for empty searches*/
        if (!query.trim())
            return;

        setLoading(true);

        try {
            const found = await searchShows(query);
            setResults(filterRelevantResults(found ?? [], query));
        } catch (error) {
            console.error(error);
            setResults([]);
        } finally {
            setLoading(false);
            setHasSearched(true);
        }
    }

    function isSelected(chosen_show: Show): boolean {
        return selectedShows.some((possible_show) => possible_show.netflix_id === chosen_show.netflix_id);
    }

    return (
        <div className="search-bar">
            <form onSubmit={handleSearch}>
                <input
                    type="text"
                    value={query}
                    onChange={(event) => {
                        const value = event.target.value;
                        setQuery(value);
                        if (!value.trim()) {
                            setResults([]);
                            setHasSearched(false);
                        }
                    }}
                    placeholder="Search for a show..."
                />
                <button type="submit">Search</button>
            </form>

        {loading && <p>Searching...</p>}

        {!loading && hasSearched && results.length === 0 && (
            <p className="no-results">No shows found. Try a different title.</p>
            )}

            <ul className="search-results">
            {results.map((show) => (
                <li key={show.netflix_id}>
                <label>
                    <input
                    type="checkbox"
                    checked={isSelected(show)}
                    onChange={() => onToggleShow(show)}
                    />
                    {show.title}
                </label>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default SearchBar;