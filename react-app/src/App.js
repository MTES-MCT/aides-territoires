import "./polyfill";
import React, { Component } from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./store";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import ParcoursTerritoire from "./pages/ParcoursTerritoire/ParcoursTerritoire";
import ParcoursPhase from "./pages/ParcoursPhase/ParcoursPhase";
import ResultsPage from "./pages/ResultsPage/ResultsPage";
import SearchPage from "./pages/SearchPage/SearchPage";
import AidePage from "./pages/AidePage/AidePage";
import ParcoursPhaseAvantProjet from "./pages/ParcoursPhaseAvantProjet/ParcoursPhaseAvantProjet";
import ParcoursCriteres from "./pages/ParcoursCriteres/ParcoursCriteres";

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <MuiThemeProvider>
            <div className="App">
              <Switch>
                <Route exact path="/" component={SearchPage} />
                <Route exact path="/aide" component={AidePage} />
                <Route exact path="/parcours/results" component={ResultsPage} />
                <Route exact path="/parcours/phase" component={ParcoursPhase} />
                <Route
                  exact
                  path="/parcours/phase/avant-projet"
                  component={ParcoursPhaseAvantProjet}
                />
                <Route
                  exact
                  path="/parcours/criteres"
                  component={ParcoursCriteres}
                />
              </Switch>
            </div>
          </MuiThemeProvider>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
