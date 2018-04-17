import React from "react";
import { Link } from "react-router-dom";

class Navigation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      mobileMenuIsActive: false
    };
  }
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
      <nav
        className="navbar app-main-menu"
        role="navigation"
        aria-label="main navigation"
      >
        <div className="navbar-brand">
          <Link className="navbar-item" to="/#aides-territoires">
            <img
              style={{ paddingRight: "20px" }}
              src="/static/images/logo-gouv.png "
            />{" "}
            <p className="app-name ">
              Aides-territoires.<strong>beta.gouv</strong>.fr
            </p>
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
            <Link className="navbar-item" onClick={this.handleLinkClick} to="/">
              Aides-territoires
            </Link>
            <Link
              className="navbar-item"
              onClick={this.handleLinkClick}
              to="/search"
            >
              Rechercher une aide
            </Link>
          </div>
        </div>
      </nav>
    );
  }
}

export default Navigation;
