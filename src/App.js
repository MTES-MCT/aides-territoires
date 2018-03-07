import React, { Component } from "react";
import Header from "./features/app/components/presentationals/header/Header";
import SearchPage from "./features/search/components/pages/searchPage/SearchPage";
import "bulma/css/bulma.css";

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header />
        <SearchPage />
      </div>
    );
  }
}

export default App;
