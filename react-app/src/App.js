import React from "react";
import { Route, Redirect, BrowserRouter, Switch } from "react-router-dom";
import { Provider } from "react-redux";
import { ApolloProvider } from "react-apollo";
import apolloClient from "./lib/apolloClient";
import store from "./store";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import SearchByTerritoirePage from "./components/search/SearchByTerritoirePage";
import SearchAidePage from "./components/search/SearchAidePage";
import AdminAideCreatePage from "./components/admin/AdminAideCreatePage";
import AdminAideEditPage from "./components/admin/AdminAideEditPage";
import AdminAideListPage from "./components/admin/AdminAideListPage";
import AdminPermissionsOverview from "./components/admin/AdminPermissionsOverview";
import LoginPage from "./components/auth/LoginPage";
import LogoutPage from "./components/auth/LogoutPage";

class App extends React.PureComponent {
  render() {
    return (
      <ApolloProvider client={apolloClient}>
        <Provider store={store}>
          <BrowserRouter>
            <MuiThemeProvider>
              <div className="App">
                <Switch>
                  <Route exact path="/" component={SearchByTerritoirePage} />
                  {/*backward compatibiliy*/}
                  <Redirect from="/recherche" to="/" />
                  <Route exact path="/aides" component={SearchAidePage} />
                  <Route exact path="/admin" component={AdminAideListPage} />
                  <Route
                    exact
                    path="/admin/aide/permissions"
                    component={AdminPermissionsOverview}
                  />
                  <Route
                    exact
                    path="/admin/aide/create"
                    component={AdminAideCreatePage}
                  />
                  <Route
                    exact
                    path="/admin/aide/list"
                    component={AdminAideListPage}
                  />
                  <Route
                    exact
                    path="/admin/aide/:id/edit"
                    component={AdminAideEditPage}
                  />
                  <Route exact path="/login" component={LoginPage} />
                  <Route exact path="/logout" component={LogoutPage} />
                  <Route component={() => <div>Oups ! Page non trouvée</div>} />
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
