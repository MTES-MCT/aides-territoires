import React from "react";
import PropTypes from "prop-types";
import injectSheet from "react-jss";
import classNames from "classnames";

const SuggestionList = class extends React.Component {
  static propTypes = {
    onClick: PropTypes.func,
    suggestions: PropTypes.arrayOf(
      PropTypes.shape({
        label: PropTypes.string,
        value: PropTypes.oneOfType([PropTypes.object, PropTypes.string])
      })
    ),
    // index de la suggestion active, en partant de zéro
    selectedSuggestionIndex: PropTypes.number
  };
  static defaultProps = {
    onClick: null,
    activeSuggestionIndex: 0
  };
  handleClick = (index, suggestion) => {
    if (this.props.onClick) {
      this.props.onClick(index, suggestion);
    }
  };
  render() {
    const { suggestions, classes } = this.props;
    return (
      <div className={classes.root}>
        <ul className={classes.ul}>
          {suggestions.map((suggestion, index) => (
            <li
              className={classNames(classes.li, {
                [classes.liActive]: this.props.selectedSuggestionIndex === index
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
      background: "rgba(144, 238, 144, 0.3)"
    }
  },
  liActive: {
    background: "rgba(144, 238, 144, 0.3)"
  }
};

export default injectSheet(styles)(SuggestionList);
