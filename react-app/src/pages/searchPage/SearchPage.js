import React from "react";
import DefaultLayout from "../../layouts/defaultLayout/DefaultLayout";
import SearchFormContainer from "../../containers/searchFormContainer/SearchFormContainer";
import SearchResultListContainer from "../../containers/searchResultListContainer/SearchResultListContainer";
import AppLoader from "../../presentationals/appLoader/AppLoader";
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
      searchedData: {}
    };
  }
  onSearchSubmit = values => {
    this.setState({ searchedData: values });
  };
  render() {
    return (
      <DefaultLayout>
        <div className="has-text-centered">
          <h2 className="title is-1">Où est situé votre projet ?</h2>
          <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
        </div>
        <div className="container">
          <div className="columns">
            <div className="column is-2">
              <h2 className="title is-2 has-text-centered"> </h2>
              <div>
                <Paper style={styles.Paper} zDepth={1}>
                  Ingénierie
                </Paper>
                <Paper style={styles.Paper} zDepth={1}>
                  Financement
                </Paper>
                <Paper style={styles.Paper} zDepth={1}>
                  Autres aide
                </Paper>
              </div>
            </div>
            <div className="column">
              <ReactGoogleSheetConnector
                apiKey="AIzaSyDIYvCWkj5B4LmGMeBMOuwzRuiV80nhTyg"
                spreadsheetId={"1Niopty1WMvtBXQY1wbASuCm83dq2pIIcv3LcpYbBDQo"}
                spinner={
                  <AppLoader>Connexion à la feuille Google ...</AppLoader>
                }
              >
                <div className="search-page">
                  <SearchResultListContainer
                    searchedData={this.state.searchedData}
                  />
                </div>
              </ReactGoogleSheetConnector>
            </div>
          </div>
        </div>
        <div className="has-text-centered section">
          <Link to="/parcours/phase">
            <RaisedButton label="Suivant" primary={true} />
          </Link>
        </div>
      </DefaultLayout>
    );
  }
}

export default SearchPage;
