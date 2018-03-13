import React from "react";
import PropTypes from "prop-types";
import { connectToSpreadsheet } from "react-google-sheet-connector";

class SearchResultList extends React.Component {
  render() {
    const SheetData = this.props.getSheet("version-1");
    if (this.props.searchedData.data) {
      SheetData.filter({ périmètre: this.props.searchedData.data.nom });
    }
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
        {SheetData.map((row, index) => (
          <div className="box" key={index}>
            <h2 className="title is-3">{row[1]}</h2>
            <div className="objectif">{row[5]}</div>
            <div className="tag lieu is-success">{row[4]}</div>
            <div className="tag thematique">{row[0]}</div>
          </div>
        ))}
      </div>
    );
  }
}

SearchResultList.propTypes = {
  searchedData: PropTypes.object.isRequired
};

export default connectToSpreadsheet(SearchResultList);
