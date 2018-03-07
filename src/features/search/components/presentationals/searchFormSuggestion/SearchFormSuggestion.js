import React from "react";
import PropTypes from "prop-types";

const SearchFormSuggestion = ({ suggestion }) => {
  return (
    <a href="#" className="dropdown-item">
      {suggestion}
    </a>
  );
};

SearchFormSuggestion.PropTypes = {};

export default SearchFormSuggestion;
