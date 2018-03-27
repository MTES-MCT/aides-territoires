import "./polyfill";
import React, { Component } from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import HomePage from "./features/app/components/pages/homePage/HomePage";
import SearchPage from "./features/search/components/pages/searchPage/SearchPage";
import ParcoursPage from "./features/parcours/components/pages/parcoursPage/ParcoursPages";

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <Switch>
            <Route exact path="/" component={HomePage} />
            <Route exact path="/search" component={SearchPage} />
            <Route exact path="/parcours" component={ParcoursPage} />
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
