import React from "react";
import PropTypes from "prop-types";
import "./TextSuggestions.css";

export default class extends React.Component {
  static propTypes = {
    onSuggestionClick: PropTypes.func.isRequired
  };
  render() {
    const { suggestions } = this.props;
    return (
      <div className="TextSuggestions dropdown is-active">
        <ul className="suggestionsWrapper">
          {suggestions.map((suggestion, index) => (
            <li
              onClick={e => this.props.onSuggestionClick(suggestion)}
              key={index}
            >
              {suggestion.label}
            </li>
          ))}
        </ul>
      </div>
    );
  }
}
