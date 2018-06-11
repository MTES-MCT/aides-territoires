import React from "react";
import injectSheet from "react-jss";
import uiConfig from "../../ui.config";
import PropTypes from "prop-types";

const Section = ({ classes, children }) => {
  return <div className={classes.root}>{children}</div>;
};

const styles = {
  root: {
    padding: "4rem",
    background: ({ type }) => {
      let color = uiConfig.colors.primary;
      if (type === "secondary") {
        color = uiConfig.colors.secondary;
      }
      return color;
    }
  }
};

Section.propTypes = {
  type: PropTypes.oneOf(["primary", "secondary"])
};

export default injectSheet(styles)(Section);
