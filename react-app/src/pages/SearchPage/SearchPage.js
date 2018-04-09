import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import SearchFormContainer from "../../containers/SearchFormContainer/SearchFormContainer";
import SearchResultListContainer from "../../containers/SearchResultListContainer/SearchResultListContainer";
import AppLoader from "../../presentationals/AppLoader/AppLoader";
import ReactGoogleSheetConnector from "react-google-sheet-connector";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";
import Paper from "material-ui/Paper";

const styles = {
  Paper: {
    height: 150,
    width: 150,
    margin: 20,
    textAlign: "center",
    display: "inline-block",
    padding: 10
  }
};

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
      <DefaultLayout>
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
      </DefaultLayout>
    );
  }
}

export default SearchPage;
