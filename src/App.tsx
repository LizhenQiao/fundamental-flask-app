import React from "react";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";

import Login from "./pages/login";
import Upload from "./pages/upload";
import Home from "./pages/home";

function App() {
  return (
    <div className="App">
      <header className="App-header"></header>
      <BrowserRouter>
        <Switch>
          <Route exact path="/">
            <Home></Home>
          </Route>
          <Route path="/login">
            <Login></Login>
          </Route>
          <Route path="/upload">
            <Upload></Upload>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
