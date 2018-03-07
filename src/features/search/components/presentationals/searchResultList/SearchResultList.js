import React from "react";
import PropTypes from "prop-types";

class SearchResultList extends React.Component {
  render() {
    return (
      <div className="search-result-list section container">
        {this.props.searchedData.text && (
          <div className="box">
            <h2>Liste des aides pour </h2>
            <pre>{JSON.stringify(this.props.searchedData)}</pre>
          </div>
        )}
      </div>
    );
  }
}

SearchResultList.propTypes = {
  searchedData: PropTypes.object.isRequired
};

export default SearchResultList;
