import "./polyfill";
import React, { Component } from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import HomePage from "./features/app/components/pages/homePage/HomePage";
import SearchPage from "./features/search/components/pages/searchPage/SearchPage";
import ParcoursPage from "./features/parcours/components/pages/parcoursPage/ParcoursPage";

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <Switch>
            <Route exact path="/" component={HomePage} />
            <Route exact path="/search" component={SearchPage} />
            <Route path="/parcours/:step?" component={ParcoursPage} />
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
