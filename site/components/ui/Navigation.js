import React from "react";
import Link from "next/link";
import PropTypes from "prop-types";
import Container from "./Container";
import imageLogoAidesTerritoires from "../../static/images/logo-aides-territoires.png";
import imageLogoFabriqueNumerique from "../../static/images/logo-fabrique-numerique.svg";
import InjectSheet from "react-jss";
import uiConfig from "../../ui.config";

let Navigation = class extends React.Component {
  state = {
    mobileMenuOpened: false
  };
  static propTypes = {
    links: PropTypes.arrayOf(
      PropTypes.shape({
        to: PropTypes.string.isRequired,
        title: PropTypes.string.isRequired
      }).isRequired
    )
  };
  render() {
    const { classes, links } = this.props;
    return (
      <div className={classes.root}>
        <div className={classes.regionLogos}>
          <MenuLogoAidesTerritoires />
          <MenuLogoFabriqueNumerique />
        </div>
        <div className={classes.regionLinks}>
          <MenuRight links={links} />
        </div>
      </div>
    );
  }
};
Navigation = InjectSheet({
  root: {
    padding: "1rem 0",
    display: "flex",
    justifyContent: "space-between",
    position: "relative"
  },
  [uiConfig.breakpoints.smallScreen]: {
    root: {
      display: "block",
      textAlign: "center"
    },
    navigationContainer: {
      display: "block"
    }
  }
})(Navigation);

/**
 * MenuRight
 */
let MenuRight = ({ links, classes }) => (
  <div className={classes.root}>
    <ul className={classes.linksUl}>
      {links.map(link => (
        <li key={link.to} className={classes.linksLi}>
          <Link href={link.to}>
            <a className={classes.a}>{link.title}</a>
          </Link>
        </li>
      ))}
    </ul>
  </div>
);
MenuRight = InjectSheet({
  linksUl: {
    margin: 0,
    padding: 0,
    paddingTop: "1rem",
    listStyleType: "none",
    display: "flex",
    justifyContent: "space-around"
  },
  a: {
    color: "black",
    textDecoration: "none",
    padding: "1rem",
    fontSize: "18px",
    "&:hover": {
      background: "rgb(240, 240, 240)"
    }
  },
  [uiConfig.breakpoints.smallScreen]: {
    a: {
      display: "block",
      padding: "0.5rem 0",
      margin: 0
    },
    linksUl: {
      // disable flex
      display: "block"
    },
    linksLi: {
      display: "block",
      textAlign: "center"
    }
  }
})(MenuRight);

let MenuLogoAidesTerritoires = ({ classes }) => {
  return (
    <img
      alt="Logo aides territoires"
      className={classes.image}
      alt="logo"
      src={imageLogoAidesTerritoires}
    />
  );
};
MenuLogoAidesTerritoires = InjectSheet({
  image: {
    height: "50px"
  },
  [uiConfig.breakpoints.smallScreen]: {
    image: {
      display: "Block",
      margin: "auto",
      height: "30px"
    }
  }
})(MenuLogoAidesTerritoires);

let MenuLogoFabriqueNumerique = ({ classes }) => {
  return (
    <img
      className={classes.image}
      alt="logo"
      src={imageLogoFabriqueNumerique}
    />
  );
};
MenuLogoFabriqueNumerique = InjectSheet({
  image: {
    width: "50px",
    paddingLeft: "2rem"
  },
  [uiConfig.breakpoints.smallScreen]: {
    image: {
      display: "Block",
      margin: "auto",
      width: "90px"
    }
  }
})(MenuLogoFabriqueNumerique);
export default Navigation;
