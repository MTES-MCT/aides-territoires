import React from "react";
import PropTypes from "prop-types";
import "./TextSuggestions.css";

export default class extends React.Component {
  state = {
    selectedIndex: 0
  };
  static propTypes = {
    onSuggestionClick: PropTypes.func.isRequired
  };
  static getDerivedStateFromProps(nextProps, prevState) {
    const max = nextProps.suggestions.length - 1;
    if (nextProps.inputKeyDown === "Enter") {
      nextProps.onSuggestionClick(
        nextProps.suggestions[prevState.selectedIndex]
      );
      return prevState;
    }
    if (nextProps.inputKeyDown === "ArrowDown") {
      return {
        ...prevState,
        selectedIndex:
          ++prevState.selectedIndex < max ? prevState.selectedIndex : max
      };
    }
    if (nextProps.inputKeyDown === "ArrowUp") {
      return {
        ...prevState,
        selectedIndex:
          --prevState.selectedIndex > 0 ? prevState.selectedIndex : 0
      };
    }
    return prevState;
  }
  render() {
    const { suggestions } = this.props;
    return (
      <div className="TextSuggestions dropdown is-active">
        <ul className="suggestionsWrapper">
          {suggestions.map((suggestion, index) => (
            <li
              className={this.state.selectedIndex === index ? "active" : ""}
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
