import React from "react";
import injectSheet from "react-jss";
import uiConfig from "../../ui.config";
import PropTypes from "prop-types";

const Section = ({ classes, children }) => {
  return <div className={classes.root}>{children}</div>;
};

const styles = {
  root: {
    padding: "6rem 0rem",
    background: ({ backgroundColor }) => {
      let color = backgroundColor;
      if (backgroundColor === "default") {
        color = uiConfig.colors.light;
      }
      if (backgroundColor === "primary") {
        color = uiConfig.colors.primaryLight;
      }
      if (backgroundColor === "secondary") {
        color = uiConfig.colors.secondary;
      }
      return color;
    }
  }
};

Section.propTypes = {
  backgroundColor: PropTypes.oneOf(["default", "primary", "secondary"])
};

Section.defaultProps = {
  backgroundColor: "default"
};

export default injectSheet(styles)(Section);
