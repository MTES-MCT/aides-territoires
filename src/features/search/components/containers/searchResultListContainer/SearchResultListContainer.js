import React from "react";
import PropTypes from "prop-types";
import SearchResultList from "../../presentationals/searchResultList/SearchResultList";
import { connectToSpreadsheet } from "react-google-sheet-connector";

class SearchResultListContainer extends React.Component {
  render() {
    const SheetData = this.props.getSheet("version-1");
    if (this.props.searchedData.data) {
      SheetData.filter({ périmètre: this.props.searchedData.data.nom });
    }
    const results = SheetData.getCurrentData();
    // SheetData.map(r => console.log(r));
    return (
      <div className="search-result-list section container">
        <div className="debug">
          {this.props.searchedData.text && (
            <div className="box">
              <h2>Liste des aides pour </h2>
              <pre>{JSON.stringify(this.props.searchedData)}</pre>
            </div>
          )}
        </div>
        <SearchResultList {...this.props} results={results} />
      </div>
    );
  }
}

SearchResultListContainer.propTypes = {
  searchedData: PropTypes.object.isRequired
};

export default connectToSpreadsheet(SearchResultListContainer);
