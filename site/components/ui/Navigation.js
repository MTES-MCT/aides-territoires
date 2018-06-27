import React from "react";
import Link from "next/link";
import PropTypes from "prop-types";
import imageLogoAidesTerritoires from "../../static/images/logo-aides-territoires.png";
import imageLogoFabriqueNumerique from "../../static/images/logo-fabrique-numerique.svg";
import InjectSheet from "react-jss";
import uiConfig from "../../ui.config";
import Beta from "./Beta";

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
        <div className={classes.navRegion}>
          <Link href="/">
            <a>
              <MenuLogoAidesTerritoires />
              <MenuLogoFabriqueNumerique />
            </a>
          </Link>
        </div>
        <div className={classes.navRegion}>
          <Beta />
        </div>
        <div className={classes.navRegion}>
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
  navRegion: {
    //border: "solid red 1px"
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
    marginRight: "1rem",
    padding: 0,
    listStyleType: "none",
    display: "flex",
    justifyContent: "space-around"
  },
  a: {
    color: "black",
    fontWeight: "200",
    textDecoration: "none",
    borderRadius: "5px",
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
    padding: "0 1rem",
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
    width: "50px"
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
