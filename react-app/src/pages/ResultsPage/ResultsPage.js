import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import SearchFormContainer from "../../containers/SearchFormContainer/SearchFormContainer";
import SearchResultListContainer from "../../containers/SearchResultListContainer/SearchResultListContainer";
import AppLoader from "../../presentationals/AppLoader/AppLoader";
import ReactGoogleSheetConnector from "react-google-sheet-connector";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";
import Paper from "material-ui/Paper";
import queryString from "query-string";
import { getTerritoireByTypeAndCodeInsee } from "../../services/geoApi";

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

class ResultsPage extends React.Component {
  constructor(props) {
    let searchedData = null;
    if (props.location.search) {
      const params = queryString.parse(props.location.search);
      searchedData = JSON.parse(params.searchedData);
      console.log("searchedData", searchedData);
    }
    super(props);
    this.state = {
      searchedData
    };
  }
  onSearchSubmit = values => {
    this.setState({ searchedData: values });
  };
  render() {
    return (
      <DefaultLayout>
        <div className="has-text-centered">
          <h2 className="title is-1">Les aides</h2>
          <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
        </div>
        {this.state.searchedData && (
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
                  spinner={<AppLoader>Recherche de résultats ...</AppLoader>}
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
        )}
        <div className="has-text-centered section">
          <Link style={{ margin: "12px" }} to="/">
            <RaisedButton label="Précédent" secondary={true} />
          </Link>
          <Link to="/parcours/criteres">
            <RaisedButton label="Affiner les résultats" primary={true} />
          </Link>
        </div>
      </DefaultLayout>
    );
  }
}

export default ResultsPage;
