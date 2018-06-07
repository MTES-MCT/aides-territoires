import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import injectSheet from "react-jss";
import headerBackground from "../../images/header-5.png";

const Header = ({ classes, data }) => {
  return (
    <header className={classes.header} id="aides-territoires">
      <div className={classes.headerOverlay}>
        <h1 className={classes.title}>{data.headertitre}</h1>
        <h2
          className={classes.subtitle}
          dangerouslySetInnerHTML={{ __html: data.header }}
        />
        <div className="button is-large is-primary">
          <Link className={classes.button} to="/recherche">
            Lancer la recherche
          </Link>
        </div>
      </div>
    </header>
  );
};

Header.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.string,
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
