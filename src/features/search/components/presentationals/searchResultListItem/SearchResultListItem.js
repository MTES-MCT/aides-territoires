import React from "react";
import PropTypes from "prop-types";

class SearchResultListItem extends React.Component {
  render() {
    const { result } = this.props;
    return (
      <div className="search-result-list-item box">
        <h2 className="title is-3">{result[1]}</h2>
        <div className="objectif">{result[5]}</div>
        <div className="tag lieu is-success">{result[4]}</div>
        <div className="tag thematique">{result[0]}</div>
      </div>
    );
  }
}

SearchResultListItem.propTypes = {
  result: PropTypes.array.isRequired
};

export default SearchResultListItem;
