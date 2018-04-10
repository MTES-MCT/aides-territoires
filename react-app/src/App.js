import "./polyfill";
import React, { Component } from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./store";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import HomePage from "./modules/homepage/pages/HomePage";
import SearchPage from "./modules/search/pages/SearchPage";

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <MuiThemeProvider>
            <div className="App">
              <Switch>
                <Route exact path="/" component={HomePage} />
                <Route exact path="/search" component={SearchPage} />
              </Switch>
            </div>
          </MuiThemeProvider>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
