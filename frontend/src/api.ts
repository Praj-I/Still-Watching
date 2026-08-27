const BASE_URL = "http://127.0.0.1:8000";

export interface Show {
    netflix_id: number;
    title: string;
}

/*Asynchrnous functions*/
export async function searchShows(title: string): Promise<Show[]> {
    const response = await fetch(`${BASE_URL}/search?title=${encodeURIComponent(title)}`);

    if (!response.ok)
        throw new Error("Search failed.");

    return response.json();
}

export async function getTrackedShows(): Promise<Show[]> {
    const response = await fetch(`${BASE_URL}/shows`);
    if (!response.ok)
        throw new Error("Failed to load shows.");

    return response.json();
}

export async function getNotificationEmail(): Promise<string | null> {
    const response = await fetch(`${BASE_URL}/settings/email`);

    if (!response.ok)
        throw new Error("Failed to load email");

    const data = await response.json();
    return data.email;
}

export async function initialSetup(shows: Show[], email: string): Promise<void> {
    const response = await fetch(`${BASE_URL}/settings/setup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ show_list: shows, email }),
    });

    if (!response.ok)
        throw new Error("Setup failed");
}

export async function addShows(shows: Show[]): Promise<void> {
    const response = await fetch(`${BASE_URL}/shows`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ show_list: shows }),
    });

    if (!response.ok)
        throw new Error("Adding shows failed");
}

export async function deleteShow(netflixId: number): Promise<void> {
    const response = await fetch(`${BASE_URL}/shows/${netflixId}`, {
        method: "DELETE",
    });

    if (!response.ok)
        throw new Error("Delete failed");
}