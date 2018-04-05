import React from "react";
import PropTypes from "prop-types";
import SearchResultList from "../../presentationals/searchResultList/SearchResultList";
import { connectToSpreadsheet } from "react-google-sheet-connector";

class SearchResultListContainer extends React.Component {
  constructor(props) {
    super(props);
    this.sheetData = this.props.getSheet("version-2");
    this.codeCommune = null;
    this.codeDepartement = null;
    this.codeRegion = null;
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
    if (Object.keys(this.props.searchedData).length === 0) {
      return <div />;
    }
    let resultsGroups = [];
    if (this.props.searchedData.type === "commune") {
      this.codeCommune = this.props.searchedData.data.code;
      this.codeDepartement = this.props.searchedData.data.codeDepartement;
      this.codeRegion = this.props.searchedData.data.codeRegion;
    }
    if (this.props.searchedData.type === "departement") {
      this.codeDepartement = this.props.searchedData.data.code;
      this.codeRegion = this.props.searchedData.data.codeRegion;
    }
    if (this.props.searchedData.type === "region") {
      this.codeDepartement = this.props.searchedData.data.code;
    }
    if (this.codeCommune) {
      resultsGroups.push({
        title: "Communes",
        results: this.filterAides("commune", this.codeCommune)
      });
    }
    if (this.codeDepartement) {
      resultsGroups.push({
        title: "Département",
        results: this.filterAides("departement", this.codeDepartement)
      });
    }
    if (this.codeRegion) {
      resultsGroups.push({
        title: "Région",
        results: this.filterAides("region", this.codeRegion)
      });
    }
    resultsGroups.push({
      title: "National",
      results: this.filterAides("national")
    });
    resultsGroups.push({
      title: "Europe",
      results: this.filterAides("europe")
    });

    return (
      <div className="search-result-list">
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
            <div key={index} className="content">
              <h2 className="title is-2 is-text-centered">
                {resultsGroup.title}
              </h2>
              {resultsGroup.results.length === 0 && <div>Pas de résultat</div>}
              {resultsGroup.results && (
                <SearchResultList
                  key={index}
                  {...this.props}
                  results={resultsGroup.results}
                />
              )}
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
