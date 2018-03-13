import React from "react";
import PropTypes from "prop-types";
import SearchResultList from "../../presentationals/searchResultList/SearchResultList";
import { connectToSpreadsheet } from "react-google-sheet-connector";

class SearchResultListContainer extends React.Component {
  constructor(props) {
    super(props);
    this.sheetData = this.props.getSheet("version-2");
  }
  filterAides(type, codeInsee = null) {
    let results = [];
    this.sheetData.map(row => {
      if (!codeInsee) {
        if (row.typeDePérimètre === type) {
          results.push(row);
        }
      }
      if (codeInsee) {
        if (row.typeDePérimètre === type && row.codeInsee == codeInsee) {
          results.push(row);
        }
      }
    });
    return results;
  }
  render() {
    //SheetData.filter({ "code insee": "44109" });
    let resultsGroups = [];
    if (this.props.searchedData.type === "commune") {
      resultsGroups.push({
        title: "Communes",
        results: this.filterAides("commune", this.props.searchedData.data.code)
      });
      resultsGroups.push({
        title: "Département",
        results: this.filterAides(
          "departement",
          this.props.searchedData.data.codeDepartement
        )
      });
      resultsGroups.push({
        title: "Région",
        results: this.filterAides(
          "region",
          this.props.searchedData.data.codeRegion
        )
      });
      resultsGroups.push({
        title: "National",
        results: this.filterAides("national")
      });
      resultsGroups.push({
        title: "Europe",
        results: this.filterAides("europe")
      });
    }

    // console.log("results", results);
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
        {resultsGroups.map((resultsGroup, index) => {
          return (
            <div>
              <h2 class="container title is-5">{resultsGroup.title}</h2>
              <SearchResultList
                key={index}
                {...this.props}
                results={resultsGroup.results}
              />
            </div>
          );
        })}
      </div>
    );
  }
}

SearchResultListContainer.propTypes = {
  searchedData: PropTypes.object.isRequired
};

export default connectToSpreadsheet(SearchResultListContainer);
