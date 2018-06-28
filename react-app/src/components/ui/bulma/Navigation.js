import React from "react";
import { Link } from "react-router-dom";
import { compose } from "react-apollo";
import LogoAidesTerritoires from "../brand/LogoAidesTerritoires";
import LogoFabNum from "../brand/LogoFabNum";
import PropTypes from "prop-types";
import Beta from "../../ui/Beta";
import injectSheet from "react-jss";
import withUser from "../../decorators/withUser";

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
    const { classes, user } = this.props;
    return (
      <nav className="navbar app-main-menu" aria-label="main navigation">
        <div className="navbar-brand">
          <a
            className="navbar-item"
            href="https://www.aides-territoires.beta.gouv.fr"
          >
            <LogoAidesTerritoires className={classes.logoAidesTerritoires} />
            <LogoFabNum className={classes.logoFabNum} />{" "}
          </a>
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
          <div className="navbar-end has-text-centered">
            <Beta />
            {this.props.links.map(link => {
              return /^https?:\/\//.test(link.to) ? (
                <a key={link.to} className="navbar-item" href={link.to}>
                  {link.title}
                </a>
              ) : (
                <Link key={link.to} className="navbar-item" to={link.to}>
                  {link.title}
                </Link>
              );
            })}
            {!!user && (
              <Link className="navbar-item" to="/logout">
                Se déconnecter
              </Link>
            )}
          </div>
        </div>
      </nav>
    );
  }
}

export default compose(
  withUser(),
  injectSheet({
    logoAidesTerritoires: {
      maxHeight: "45px !important"
    },
    // override Bulma max-height img in navigation
    logoFabNum: {
      maxHeight: "80px !important",
      paddingLeft: "1rem"
    }
  })
)(Navigation);
