import React from "react";
import PropTypes from "prop-types";
import "./TextSuggestions.css";

export default class extends React.Component {
  static propTypes = {
    onClick: PropTypes.func.isRequired
  };
  handleClick = suggestion => {
    this.props.onClick(suggestion);
  };
  render() {
    const { suggestions } = this.props;
    return (
      <div className="TextSuggestions dropdown is-active">
        <ul className="suggestionsWrapper">
          {suggestions.map((suggestion, index) => (
            <li onClick={e => this.handleClick(suggestion)} key={index}>
              {suggestion.text}
            </li>
          ))}
        </ul>
      </div>
    );
  }
}
