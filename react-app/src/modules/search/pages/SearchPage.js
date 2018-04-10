import React from "react";
import ThemeDefault from "../../../themes/ThemeDefault/ThemeDefault";
import SearchFormContainer from "../decorators/SearchFormContainer";
import SearchResultListContainer from "../decorators/SearchResultListContainer";
import AppLoader from "../../generic/presentationals/AppLoader";
import ReactGoogleSheetConnector from "react-google-sheet-connector";
import Header from "../../../themes/ThemeDefault/presentationals/Header";

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchedData: null
    };
  }
  onSearchSubmit = values => {
    this.setState({ searchedData: values });
  };
  render() {
    return (
      <ThemeDefault>
        <Header />
        <section className="section container">
          <div className="has-text-centered">
            <h2 className="title is-1">Où est situé votre projet ?</h2>
            <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
          </div>
          {this.state.searchedData && (
            <div className="container">
              <div className="columns">
                <div className="column">
                  <ReactGoogleSheetConnector
                    apiKey="AIzaSyDIYvCWkj5B4LmGMeBMOuwzRuiV80nhTyg"
                    spreadsheetId={
                      "1Niopty1WMvtBXQY1wbASuCm83dq2pIIcv3LcpYbBDQo"
                    }
                    spinner={<AppLoader>Recherche de résultats ...</AppLoader>}
                  >
                    <section className="search-page">
                      <SearchResultListContainer
                        searchedData={this.state.searchedData}
                      />
                    </section>
                  </ReactGoogleSheetConnector>
                </div>
              </div>
            </div>
          )}
          {/*
        <div className="has-text-centered section">
          <Link to="/parcours/phase">
            <RaisedButton label="Suivant" primary={true} />
          </Link>
        </div>
        */}
        </section>
      </ThemeDefault>
    );
  }
}

export default SearchPage;
