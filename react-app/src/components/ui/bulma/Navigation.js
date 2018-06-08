import React from "react";
import { Link } from "react-router-dom";
import LogoAidesTerritoires from "../brand/LogoAidesTerritoires";
import LogoFabNum from "../brand/LogoFabNum";
import PropTypes from "prop-types";
import injectSheet from "react-jss";

class Navigation extends React.PureComponent {
  state = {
    mobileMenuIsActive: false
  };
  static propTypes = {
    links: PropTypes.arrayOf(
      PropTypes.shape({
        to: PropTypes.string,
        title: PropTypes.string
      }).isRequired
    )
  };
  handleClick = () => {
    this.setState({
      mobileMenuIsActive: !this.state.mobileMenuIsActive
    });
  };
  handleLinkClick = () => {
    this.setState({
      mobileMenuIsActive: false
    });
  };
  render() {
    const { classes } = this.props;
    return (
      <nav className="navbar app-main-menu" aria-label="main navigation">
        <div className="navbar-brand">
          <Link className="navbar-item" to="/#aides-territoires">
            <LogoAidesTerritoires className={classes.logoAidesTerritoires} />
            <LogoFabNum className={classes.logoFabNum} />
          </Link>
          <div
            className={
              this.state.mobileMenuIsActive
                ? "navbar-burger is-active"
                : "navbar-burger"
            }
            data-target="navMenu"
            onClick={this.handleClick}
          >
            <span />
            <span />
            <span />
          </div>
        </div>
        <div
          className={
            this.state.mobileMenuIsActive
              ? "navbar-menu is-active"
              : "navbar-menu"
          }
          id="navMenu "
        >
          <div className="navbar-end">
            {this.props.links.map(link => {
              {
                return /^https?:\/\//.test(link.to) ? (
                  <a class="navbar-item" href={link.to}>
                    {link.title}
                  </a>
                ) : (
                  <Link key={link.to} className="navbar-item" to={link.to}>
                    {link.title}
                  </Link>
                );
              }
            })}
          </div>
        </div>
      </nav>
    );
  }
}

export default injectSheet({
  logoAidesTerritoires: {
    maxHeight: "50px !important"
  },
  // override Bulma max-height img in navigation
  logoFabNum: {
    maxHeight: "80px !important",
    paddingLeft: "2rem"
  }
})(Navigation);
