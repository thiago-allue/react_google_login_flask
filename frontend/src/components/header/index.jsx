import React from 'react';
import logo from '../../assets/logo.png';

function Header({ email, activeMenu }) {
  return (
    <div>
      <div id="div_header">
        <a href="/page_homepage"><img alt="Logo" src={logo} className="logo_in_header_pages" /></a>
        <span id="h1_for_menu"><h1>Quotes Machine</h1></span>
      </div>

      <div id="div_header_menu">
        <div id="menu_entry_home">
          <span className={`menu_entry ${activeMenu === 'page_homepage' ? 'bold' : ''}`}><a href="/page_homepage" className="a_navigation" id="home_link">Home</a></span>
          <span className={`menu_entry ${activeMenu === 'page_my_quotes' ? 'bold' : ''}`}><a href="/page_my_quotes" className="a_navigation" id="my_quotes_link">My Quotes</a></span>
          <span className={`menu_entry ${activeMenu === 'page_create_quote' ? 'bold' : ''}`}><a href="/page_handcrafting" className="a_navigation" id="handcrafting_link">Handcrafting</a></span>
          <span className={`menu_entry ${activeMenu === 'page_gen_ai' ? 'bold' : ''}`}><a href="/page_gen_ai" className="a_navigation" id="gen_ai_link">GenAI</a></span>
        </div>
      </div>

      <p className="header">
        {console.log(email)}
        {console.log({email})}
        <span className="span_user">{email}</span>
        <a href="/logout" className="a_logout">, Logout</a>
      </p>
    </div>
  );
}

export default Header;
