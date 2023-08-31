import axios from 'axios';

const BASE_URL = 'http://localhost:5000'; // Flask server URL

export let loginUser;
loginUser = async (email, password) => {
    const response = await axios.post(`${BASE_URL}/login`, {email, password});
    return response.data;
};

// Add other API calls as needed...
