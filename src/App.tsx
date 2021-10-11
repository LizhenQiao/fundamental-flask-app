import React, { useEffect, useState } from "react";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";
import { Redirect } from "react-router";

import Login from "./pages/login";
import AlbumPage from "./pages/album";
import HomePage from "./pages/home";
import AdminPage from "./pages/admin";
import Logout from "./components/logout";
import checkLogin from "./utils/checkLogin";

function App() {
  const [redirectToLoginPage, setRedirectToLoginPage] = useState(false);

  // Globally check the login status. If not login, redirect to login page.
  useEffect(() => {
    if (!checkLogin()) {
      setRedirectToLoginPage(true);
    }
  }, []);

  return (
    <div className="App">
      <header className="App-header"></header>
      <BrowserRouter>
        <Switch>
          <Route exact path="/">
            <HomePage></HomePage>
            <Logout />
          </Route>
          <Route path="/home">
            <HomePage></HomePage>
            <Logout />
          </Route>
          <Route path="/admin">
            <AdminPage></AdminPage>
            <Logout />
          </Route>
          <Route path="/login">
            <Login></Login>
          </Route>
          <Route path="/album">
            <AlbumPage></AlbumPage>
            <Logout />
          </Route>
        </Switch>
        {redirectToLoginPage && <Redirect to="/login" />}
      </BrowserRouter>
    </div>
  );
}

export default App;
