import React from "react";
import PropTypes from "prop-types";

class SearchResultListItem extends React.Component {
  render() {
    const { result } = this.props;
    return (
      <div className="search-result-list-item box">
        <h2 className="title is-3">{result.intitulé}</h2>
        <div className="objectif">{result.objectifs}</div>
        <div className="tag lieu is-success">{result.périmètre}</div>
        <div className="tag thematique">{result.sousThématique}</div>
      </div>
    );
  }
}

SearchResultListItem.propTypes = {
  result: PropTypes.array.isRequired
};

export default SearchResultListItem;
