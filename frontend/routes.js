import React from "react";
import {useRoutes} from "react-router-dom";
import HomePage from "./pages/home";
import LoginScreen from "./pages/login_screen";


function Routes() {
    return useRoutes([
        {path: "/", element: <LoginScreen/>},
        {path: "/page_homepage", element: <HomePage/>},
    ])
}

export default Routes;
