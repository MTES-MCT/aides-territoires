import React from "react";
import SearchFormSuggestion from "./SearchFormSuggestion";
import PropTypes from "prop-types";
import injectSheet from "react-jss";

const styles = {
  dropdown: {
    width: "100%"
  },
  dropdownMenu: {
    width: "100%",
    position: "relative"
  },
  dropdownContent: {
    width: "100%",
    padding: 0
  }
};

const SearchFormSuggestionList = ({
  classes,
  suggestions,
  onSuggestionClick
}) => {
  return (
    <div className={`dropdown is-active ${classes.dropdown}`}>
      <div className={`dropdown-menu ${classes.dropdownMenu}`} role="menu">
        <div className={`dropdown-content ${classes.dropdownContent}`}>
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

export default injectSheet(styles)(SearchFormSuggestionList);
