import React from "react";
import SearchFormContainer from "../../containers/searchFormContainer/SearchFormContainer";
import ReactGoogleSheetConnector from "react-google-sheet-connector";
import SearchResultListContainer from "../../containers/searchResultListContainer/SearchResultListContainer";
import PageLoader from "../../../../../features/app/components/presentationals/pageLoader/PageLoader";

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
      <ReactGoogleSheetConnector
        apiKey="AIzaSyDIYvCWkj5B4LmGMeBMOuwzRuiV80nhTyg"
        spreadsheetId={"1Niopty1WMvtBXQY1wbASuCm83dq2pIIcv3LcpYbBDQo"}
        spinner={<PageLoader>Connexion à la feuille Google ...</PageLoader>}
      >
        <div className="search-page">
          <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
          <SearchResultListContainer searchedData={this.state.searchedData} />
        </div>
      </ReactGoogleSheetConnector>
    );
  }
}

export default SearchPage;
