import React from "react";
import Link from "next/link";
import injectSheet from "react-jss";
import PropTypes from "prop-types";

const Container = ({ children, classes }) => (
  <div className={classes.root}>{children}</div>
);

export default injectSheet({
  root: {
    maxWidth: "940px",
    margin: "auto"
  }
})(Container);
