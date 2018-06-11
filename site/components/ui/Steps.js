import React from "react";
import injectSheet from "react-jss";
import PropTypes from "prop-types";

const Steps = ({ classes, children, steps, type = "primary" }) => {
  return <div className={classes.root}>{children}</div>;
};

const styles = {
  root: {
    padding: "2rem"
  }
};

export default injectSheet(styles)(Steps);
