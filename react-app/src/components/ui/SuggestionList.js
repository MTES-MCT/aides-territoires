import React from "react";
import PropTypes from "prop-types";
import injectSheet from "react-jss";
import classNames from "classnames";

const SuggestionList = class extends React.Component {
  static propTypes = {
    onClick: PropTypes.func,
    activeSuggestion: PropTypes.string,
    suggestions: PropTypes.arrayOf(
      PropTypes.shape({
        label: PropTypes.string,
        value: PropTypes.oneOfType([PropTypes.object, PropTypes.string])
      })
    )
  };
  state = {
    selectedIndex: 0,
    value: ""
  };
  handleClick = (index, suggestion) => {
    this.setState({ selectedIndex: index });
    if (this.props.onClick) {
      this.props.onClick(suggestion);
    }
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
    const { suggestions, classes } = this.props;
    return (
      <div className={classes.root}>
        <ul className={classes.ul}>
          {suggestions.map((suggestion, index) => (
            <li
              className={classNames(classes.li, {
                [classes.liActive]: this.state.selectedIndex === index
              })}
              onClick={() => this.handleClick(index, suggestion)}
              key={index}
            >
              {suggestion.label}
            </li>
          ))}
        </ul>
      </div>
    );
  }
};

const styles = {
  ul: {
    boxShadow: "0px 0px 40px 0px rgba(0, 0, 0, 0.3);"
  },
  li: {
    borderBottom: "solid silver 1px",
    borderLeft: "solid silver 1px",
    borderRight: "solid silver 1px",
    padding: "1rem",
    "&:hover": {
      cursor: "pointer",
      background: "rgba(144, 238, 144, 0.1)"
    }
  },
  liActive: {
    background: "rgba(144, 238, 144, 0.3)"
  }
};

export default injectSheet(styles)(SuggestionList);
