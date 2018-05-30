import React from "react";
import PropTypes from "prop-types";
import classnames from "classnames";
import injectSheet from "react-jss";

const styles = {
  suggestion: {
    cursor: "pointer",
    fontSize: "1.3rem",
    borderBottom: "solid silver 1px",
    padding: "0.7rem",
    "&:hover": {
      background: "rgba(32, 156, 238, 0.7)",
      color: "white"
    }
  }
};

const SearchFormSuggestion = ({ classes, suggestion, onSuggestionClick }) => {
  return (
    <div
      style={styles.suggestion}
      onClick={() => onSuggestionClick(suggestion)}
      className={classnames("dropdown-item", classes.suggestion)}
    >
      {suggestion.texte}
    </div>
  );
};

SearchFormSuggestion.propTypes = {
  onSuggestionClick: PropTypes.func.isRequired
};

export default injectSheet(styles)(SearchFormSuggestion);
