import React from "react";
import injectSheet from "react-jss";
import uiConfig from "../../ui.config";
import Link from "next/link";
import PropTypes from "prop-types";

const ButtonLink = ({ classes, children, href }) => {
  return (
    <Link href={href}>
      <a className={classes.a}>{children}</a>
    </Link>
  );
};

ButtonLink.propTypes = {
  href: PropTypes.string.isRequired,
  type: PropTypes.oneOf(["primary", "secondary"])
};

ButtonLink.defaultProps = {
  type: "primary"
};

const styles = {
  a: {
    textDecoration: "none",
    borderRadius: "5px",
    color: "white",
    fontSize: "24px",
    display: "inline-block",
    padding: "1.5rem 1.5rem",
    background: ({ type }) => {
      let color = uiConfig.colors.primaryLight;
      if (type === "secondary") {
        color = uiConfig.colors.secondary;
      }
      return color;
    },
    color: ({ type }) => {
      let color = uiConfig.colors.primary;
      if (type === "primary") {
        color = uiConfig.colors.secondary;
      }
      return color;
    }
  }
};

export default injectSheet(styles)(ButtonLink);
