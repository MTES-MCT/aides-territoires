import React from "react";
import SearchFormSuggestion from "../searchFormSuggestion/SearchFormSuggestion";
import PropTypes from "prop-types";

const SearchFormSuggestionList = ({ suggestions, onSuggestionClick }) => {
  return (
    <div className="dropdown is-active">
      <div className="dropdown-menu" role="menu">
        <div className="dropdown-content">
          {suggestions.map((suggestion, index) => {
            return (
              <SearchFormSuggestion
                key={index}
                suggestion={suggestion}
                onSuggestionClick={onSuggestionClick}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};

SearchFormSuggestionList.propTypes = {
  onSuggestionClick: PropTypes.func.isRequired
};

export default SearchFormSuggestionList;
