import React, {useEffect, useState} from 'react';
import {loginUser} from '../../api.js';
import {useNavigate} from 'react-router-dom'; // Import useNavigate from react-router-dom
import '../../style.css'
import logo_png from '../../assets/logo.png';
import google_login_png from "../../assets/google_login.png";

function LoginScreen() {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    const navigate = useNavigate();  // Create a navigate function

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        // Check if there's a token in the URL
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');

        if (token) {
            // Store the token in local storage
            localStorage.setItem('authToken', token);

            // Redirect to HomePage
            navigate('/page_homepage');
        }
    }, []);

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await loginUser(email, password);
            if (response.success) {
                setIsLoggedIn(true);
                setErrorMessage('');
                navigate('/page_homepage');
            } else {
                setErrorMessage(response.message || 'Login failed.');
            }
        } catch (error) {
            console.error("Login error:", error);
            setErrorMessage('An error occurred during login. Please try again later.');
        }
    }


    return (
        <div className="div-body-encapsulate" id="div_index">
            <img alt="Logo" src={logo_png} className="logo_in_header" />
            <div className="div-content-login">
                <h1>Login</h1>
                <br />
                {errorMessage && <div className="error-message">{errorMessage}</div>} {/* Display error message */}
                <a id="button_login_google" href={`${apiBaseUrl}/oauth/google`}>
                    <img src={google_login_png} alt="Google Logo" id="google-logo" />
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
