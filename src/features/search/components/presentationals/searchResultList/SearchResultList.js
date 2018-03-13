import React from "react";
import PropTypes from "prop-types";
import SearchResultListItem from "../searchResultListItem/SearchResultListItem";

class SearchResultList extends React.Component {
  render() {
    return (
      <div className="search-result-list section container">
        {this.props.results.map((row, index) => (
          <SearchResultListItem key={index} result={row} />
        ))}
      </div>
    );
  }
}

SearchResultList.propTypes = {
  searchedData: PropTypes.object.isRequired,
  results: PropTypes.array.isRequired
};

export default SearchResultList;
