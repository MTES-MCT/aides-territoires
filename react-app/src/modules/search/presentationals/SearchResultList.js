import React from "react";
import PropTypes from "prop-types";
import SearchResultListItem from "./SearchResultListItem";

class SearchResultList extends React.Component {
  static propTypes = {
    aides: PropTypes.array.isRequired
  };
  render() {
    return (
      <div className="search-result-list">
        {this.props.aides.map((aide, index) => (
          <SearchResultListItem key={aide.id} aide={aide} />
        ))}
      </div>
    );
  }
}

export default SearchResultList;
