import React, {useEffect, useState} from 'react';
import '../../style.css'
import logo from '../../assets/logo.png';
import Header from '../../components/header';
import {getEmail} from "../../api";

function HomePage() {
  const [quote, setQuote] = useState('');
  const [author, setAuthor] = useState('');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    // Fetch the initial quote when the component mounts
    fetchRandomQuote();

    // Fetch the user's email when the component mounts
    const fetchEmail = async () => {
      const email = await getEmail();
      if (email) {
        setUserEmail(email);
      }
    };

    fetchEmail();

  }, []);

  const fetchRandomQuote = async () => {
    // Assuming you have an endpoint in your Flask backend to get a random quote
    const response = await fetch('http://localhost:5000/get_random_quote');
    const data = await response.json();
    setQuote(data.quote);
    setAuthor(data.author);
  };

  const saveQuote = async () => {
    try {
      const response = await fetch('http://localhost:5000/save_quote', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          quote: quote,
          author: author
        })
      });

      const data = await response.json();

      if (data.success) {
        console.log("Quote saved successfully:", quote);
        // Optionally, you can update the UI to show a success message
      } else {
        console.error("Error saving quote:", data.message);
      }
    } catch (error) {
      console.error("An error occurred while saving the quote:", error);
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(prevMode => !prevMode);
  };

  return (
    <div className={`div-body-encapsulate ${isDarkMode ? 'dark-mode' : ''}`}>
      <Header email={userEmail} activeMenu="page_homepage" />
      <br/>
      <img alt="Logo" src={logo} className="logo_in_header"/>
      <br/><br/>
      <h3>Inspirational Quotes</h3>

      <div className="quote-block home-quote-block">
        <p className="quote-content p_quote">{quote}</p>
        <p className="quote-author quote-author-homepage">{author}</p>
      </div>

      <div className="button-container">
        <button onClick={saveQuote} id="loveItButton">Love it</button>
        <button onClick={fetchRandomQuote}>One More</button>
      </div>
      <p id="saveMessage" style={{color: 'green', fontWeight: 'bold', display: 'none'}}>Quote saved</p>

      <br/><br/><br/><br/><br/>
      <div className="toggle-dark-mode-container">
        <button onClick={toggleDarkMode}>
          {isDarkMode ? '☀️ Day Mode' : '🌙 Night Mode'}
        </button>
      </div>
      <span className="span_example_javascripts">Note: Examples of Vanilla Javascript Usage</span>
      <br/><br/><br/><br/><br/>
    </div>
  );
}

export default HomePage;
