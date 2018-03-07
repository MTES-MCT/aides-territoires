import React, { Component } from "react";
import Header from "./features/app/components/presentationals/header/Header";
import SearchPage from "./features/search/components/pages/searchPage/SearchPage";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import "bulma/css/bulma.css";

class App extends Component {
  render() {
    return (
      <MuiThemeProvider>
        <div className="App">
          <Header />
          <SearchPage />
        </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
