import React from "react";
import PropTypes from "prop-types";

const SearchFormSuggestion = ({ suggestion, onSuggestionClick }) => {
  return (
    <a onClick={() => onSuggestionClick(suggestion)} className="dropdown-item">
      {suggestion.text}
    </a>
  );
};

SearchFormSuggestion.propTypes = {
  onSuggestionClick: PropTypes.func.isRequired
};

export default SearchFormSuggestion;
