import React from "react";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";

import Login from "./pages/login";
import AlbumPage from "./pages/album";
import HomePage from "./pages/home";
import AdminPage from "./pages/admin";

function App() {
  return (
    <div className="App">
      <header className="App-header"></header>
      <BrowserRouter>
        <Switch>
          <Route exact path="/">
            <HomePage></HomePage>
          </Route>
          <Route path="/home">
            <HomePage></HomePage>
          </Route>
          <Route path="/admin">
            <AdminPage></AdminPage>
          </Route>
          <Route path="/login">
            <Login></Login>
          </Route>
          <Route path="/album">
            <AlbumPage></AlbumPage>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
