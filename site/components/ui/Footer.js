import React from "react";
import injectSheet from "react-jss";
import uiConfig from "../../ui.config";
import Link from "next/link";
import PropTypes from "prop-types";

const Footer = ({ classes, children, href }) => {
  return (
    <div className={classes.root}>
      Une solution Open Source propulsée avec ❤ par le Ministère de la
      Transition écologique et solidaire & Cohésion des territoires incubé grâce
      à beta.gouv.fr
    </div>
  );
};

const styles = {
  root: {
    color: uiConfig.colors.secondary,
    textAlign: "center",
    fontSize: "12px",
    background: "#444",
    padding: "2rem"
  }
};

export default injectSheet(styles)(Footer);
