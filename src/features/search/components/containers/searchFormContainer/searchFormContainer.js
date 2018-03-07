import React from "react";
import PropTypes from "prop-types";
import SearchForm from "../../presentationals/searchForm/SearchForm";
import { isPostalCode } from "../../../lib/searchLib";

class SearchFormContainer extends React.Component {
  onSubmit = values => {
    console.log(isPostalCode(values.text));
  };
  render() {
    return (
      <div className="search-form-container">
        <SearchForm onSubmit={this.onSubmit} />
      </div>
    );
  }
}

SearchFormContainer.propTypes = {};

export default SearchFormContainer;
