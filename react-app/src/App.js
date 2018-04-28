import "./polyfill";
import React, { Component } from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import { Provider } from "react-redux";
import { ApolloProvider } from "react-apollo";
import apolloClient from "./services/apolloClient";
import store from "./store";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import HomePage from "./modules/homepage/pages/HomePage";
import SearchPage from "./modules/search/pages/SearchPage";
import AideCreatePage from "./modules/admin/pages/AideCreatePage";
import AideEditPage from "./modules/admin/pages/AideEditPage";
import AdminPage from "./modules/admin/pages/AdminPage";
import AideListPage from "./modules/admin/pages/AideListPage";
import TypeDeTerritoireCreatePage from "./modules/aide/pages/TypeDeTerritoireCreatePage";

class App extends Component {
  render() {
    return (
      <ApolloProvider client={apolloClient}>
        <Provider store={store}>
          <BrowserRouter>
            <MuiThemeProvider>
              <div className="App">
                <Switch>
                  <Route exact path="/" component={HomePage} />
                  <Route exact path="/search" component={SearchPage} />
                  <Route exact path="/admin" component={AdminPage} />
                  <Route exact path="/aide/create" component={AideCreatePage} />
                  <Route exact path="/aide/list" component={AideListPage} />
                  <Route exact path="/aide/:id/edit" component={AideEditPage} />
                  <Route
                    exact
                    path="/type-de-territoire/create"
                    component={TypeDeTerritoireCreatePage}
                  />
                </Switch>
              </div>
            </MuiThemeProvider>
          </BrowserRouter>
        </Provider>
      </ApolloProvider>
    );
  }
}

export default App;
