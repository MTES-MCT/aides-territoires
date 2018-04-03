import React from "react";
import DefaultLayout from "../../layouts/defaultLayout/DefaultLayout";
import SearchFormContainer from "../../containers/searchFormContainer/SearchFormContainer";
import SearchResultListContainer from "../../containers/searchResultListContainer/SearchResultListContainer";
import AppLoader from "../../presentationals/appLoader/AppLoader";
import ReactGoogleSheetConnector from "react-google-sheet-connector";

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
        <ReactGoogleSheetConnector
          apiKey="AIzaSyDIYvCWkj5B4LmGMeBMOuwzRuiV80nhTyg"
          spreadsheetId={"1Niopty1WMvtBXQY1wbASuCm83dq2pIIcv3LcpYbBDQo"}
          spinner={<AppLoader>Connexion à la feuille Google ...</AppLoader>}
        >
          <div className="search-page">
            <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
            <SearchResultListContainer searchedData={this.state.searchedData} />
          </div>
        </ReactGoogleSheetConnector>
      </DefaultLayout>
    );
  }
}

export default SearchPage;
