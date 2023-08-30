import React, { useState } from 'react';
import axios from '../../src/api'; // Assuming you have set up axios for API calls

function LoginScreen() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false); // State to check if user is logged in
    const [errorMessage, setErrorMessage] = useState(''); // State to display error messages

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.loginUser(email, password);
            if (response.status === 200) {
                setIsLoggedIn(true); // Set user as logged in
                setErrorMessage(''); // Clear any previous error messages
            } else {
                setErrorMessage('Invalid email or password. Please try again.'); // Display error message
            }
        } catch (error) {
            console.error("Login error:", error);
            setErrorMessage('An error occurred during login_screen. Please try again later.'); // Display error message
        }
    }

    if (isLoggedIn) {
        // If user is logged in, redirect to the homepage (or any other component)
        return <Redirect to="/homepage" />; // Assuming you're using react-router-dom for routing
    }

    return (
        <div className="div-body-encapsulate" id="div_index">
            <img alt="Logo" src="/static/logo.png" className="logo_in_header" />
            <div className="div-content-login">
                <h1>Login</h1>
                <br />
                <a id="button_login_google" href="/oauth/google_login">
                    <img src="static/google_login.png" alt="Google Logo" id="google-logo" />
                    <div className="default_input_box" id="button_login_google">Login with Google</div>
                </a>
                <span className="span_example_javascripts">Note: Example of OAuth login flow usage</span>
                <p>
                    ------- or -------
                    <br />
                    <br />
                    Log in using email address
                </p>

                <form id="login-form" onSubmit={handleLogin}>
                    <input
                        type="text"
                        id="email"
                        className="default_input_box"
                        name="email"
                        required
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <br />
                    <input
                        type="password"
                        id="password"
                        className="default_input_box"
                        name="password"
                        placeholder="Password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <br />
                    <span className="span_example_javascripts">Note: Example of our server located login flow usage</span>
                    <br /><br /><br />
                    <button type="submit">Login</button>
                </form>
            </div>
        </div>
    );
}

export default LoginScreen;
