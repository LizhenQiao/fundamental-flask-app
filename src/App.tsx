import React from "react";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";

import Login from "./pages/login";
import UploadPage from "./pages/upload";
import HomePage from "./pages/home";

function App() {
  return (
    <div className="App">
      <header className="App-header"></header>
      <BrowserRouter>
        <Switch>
          <Route exact path="/">
            <HomePage></HomePage>
          </Route>
          <Route path="/login">
            <Login></Login>
          </Route>
          <Route path="/upload">
            <UploadPage></UploadPage>
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
