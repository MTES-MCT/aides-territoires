import React from "react";
import { Link, BrowserRouter } from "react-router-dom";
import PropTypes from "prop-types";
import injectSheet from "react-jss";
import headerBackground from "../../../images/header-5.png";

const Header = ({ classes, title, subtitle, callToActionText }) => {
  return (
    <header className={classes.header} id="aides-territoires">
      <div className={classes.headerOverlay}>
        <h1 className={classes.title}>{title}</h1>
        <h2 className={classes.subtitle}>{subtitle}</h2>
        {callToActionText && (
          <div className="button is-large is-primary">
            <Link className={classes.button} to="/recherche">
              {callToActionText}
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};

Header.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
  callToActionText: PropTypes.string
};

const styles = {
  header: {
    position: "relative",
    background: `url(${headerBackground})`,
    backgroundPosition: "bottom",
    backgroundSize: "cover",
    textAlign: "center",
    height: "400px"
  },
  headerOverlay: {
    paddingBottom: "5rem",
    display: "flex",
    flexDirection: "column",
    position: "absolute",
    justifyContent: "center",
    alignItems: "center",
    top: 0,
    left: 0,
    height: "100%",
    width: "100%",
    background: "rgba(20, 20, 20, 0.4)"
  },
  title: {
    fontSize: "3rem",
    lineHeight: "100%",
    color: "white"
  },
  subtitle: { color: "white", fontSize: "1rem" },
  button: { color: "white" }
};

export default injectSheet(styles)(Header);
