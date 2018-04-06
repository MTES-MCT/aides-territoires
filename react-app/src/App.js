import "./polyfill";
import React, { Component } from "react";
import { Route, BrowserRouter, Switch } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./store";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import ParcoursTerritoire from "./pages/parcoursTerritoire/ParcoursTerritoire";
import ParcoursPhase from "./pages/parcoursPhase/ParcoursPhase";
import ResultsPage from "./pages/resultsPage/ResultsPage";
import ParcoursPhaseAvantProjet from "./pages/parcoursPhaseAvantProjet/ParcoursPhaseAvantProjet";

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <MuiThemeProvider>
            <div className="App">
              <Switch>
                <Route exact path="/" component={ParcoursTerritoire} />
                <Route exact path="/parcours/results" component={ResultsPage} />
                <Route exact path="/parcours/phase" component={ParcoursPhase} />
                <Route
                  exact
                  path="/parcours/phase/avant-projet"
                  component={ParcoursPhaseAvantProjet}
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
