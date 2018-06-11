import React from "react";
import Link from "next/link";
import ButtonLink from "../ui/ButtonLink";
import Container from "./Container";
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
          <Container>
            <h1 className={classes.title}>{title}</h1>
            <h2 className={classes.subtitle}>{subtitle}</h2>
            {callToActionText && (
              <ButtonLink href={callToActionLink}>
                {callToActionText}
              </ButtonLink>
            )}
          </Container>
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

Header.defaultProps = {
  callToActionText: null,
  callToActionLink: null
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
  title: {
    fontSize: "40px",
    marginTop: "20px",
    fontWeight: "700"
  },
  subtitle: {
    marginBottom: "60px"
  },
  content: {
    padding: "1rem"
  },
  headerOverlay: {
    display: "flex",
    flexDirection: "column",
    position: "absolute",
    top: 0,
    left: 0,
    height: "100%",
    width: "100%",
    background: "rgba(20, 20, 20, 0.45)"
  },
  [uiConfig.breakpoints.smallScreen]: {
    title: {
      marginTop: "20px",
      fontSize: "22px"
    },
    subtitle: {
      fontSize: "18px",
      marginBottom: "80px"
    }
  }
  /*
  subtitle: { color: "white", fontSize: "1rem" },
  button: { color: "white" }
  */
};

export default injectSheet(styles)(Header);
