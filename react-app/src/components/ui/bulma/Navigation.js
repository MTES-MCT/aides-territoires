import React from "react";
import { Link } from "react-router-dom";
import LogoAidesTerritoires from "../brand/LogoAidesTerritoires";
import PropTypes from "prop-types";

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
    return (
      <nav className="navbar app-main-menu" aria-label="main navigation">
        <div className="navbar-brand">
          <Link className="navbar-item" to="/#aides-territoires">
            <LogoAidesTerritoires />
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
              return (
                <Link key={link.to} className="navbar-item" to={link.to}>
                  {link.title}
                </Link>
              );
            })}
          </div>
        </div>
      </nav>
    );
  }
}

export default Navigation;
