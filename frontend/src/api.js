import axios from 'axios';

const BASE_URL = 'http://localhost:5000'; // Flask server URL

export let loginUser;
loginUser = async (email, password) => {
    console.log("Try email, password:", email, password);
    const response = await axios.post(`${BASE_URL}/login`, {
        email: email,
        password: password
    }, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    console.log("response.data", response.data);
    return response.data;
};


export const getEmail = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/get_logged_in_email`, { withCredentials: true });
        return response.data.email;
    } catch (error) {
        console.error("Error fetching user's email:", error);
        return null;
    }
};


// Add other API calls as needed...
