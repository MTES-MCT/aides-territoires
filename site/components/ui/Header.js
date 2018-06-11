import React from "react";
import Link from "next/link";
import ButtonLink from "../ui/ButtonLink";
import PropTypes from "prop-types";
import injectSheet from "react-jss";
import uiConfig from "../../ui.config";

const Header = ({
  classes,
  title,
  subtitle,
  callToActionText,
  callToActionLink
}) => {
  return (
    <header className={classes.header} id="aides-territoires">
      <div className={classes.headerOverlay}>
        <div className={classes.content}>
          <h1 className={classes.title}>{title}</h1>
          <h2 className={classes.subtitle}>{subtitle}</h2>
          {callToActionText && (
            <ButtonLink href={callToActionLink}>{callToActionText}</ButtonLink>
          )}
        </div>
      </div>
    </header>
  );
};

Header.propTypes = {
  title: PropTypes.string.isRequired,
  backgroundImageUrl: PropTypes.string,
  subtitle: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
  callToActionText: PropTypes.string,
  callToActionLink: PropTypes.string
};

const styles = {
  header: {
    color: "white",
    position: "relative",
    backgroundImage: ({ backgroundImageUrl }) => `url(${backgroundImageUrl})`,
    backgroundSize: "cover",
    backgroundPosition: "bottom",
    textAlign: "center",
    height: "400px"
  },
  content: {
    padding: "1rem"
  },
  headerOverlay: {
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
  [uiConfig.breakpoints.smallScreen]: {
    content: {
      fontSize: "14px"
    }
  }
  /*
  subtitle: { color: "white", fontSize: "1rem" },
  button: { color: "white" }
  */
};

export default injectSheet(styles)(Header);
