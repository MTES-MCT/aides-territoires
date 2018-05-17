import React from "react";
import { Link } from "react-router-dom";
import Logo from "./Logo";

class Navigation extends React.PureComponent {
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
      <nav className="navbar app-main-menu" aria-label="main navigation">
        <div className="navbar-brand">
          <Link className="navbar-item" to="/#aides-territoires">
            <Logo />
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
              to="/recherche"
            >
              Rechercher une aide
            </Link>
            <a
              className="navbar-item"
              href="https://www.aides-territoires.beta.gouv.fr/#contact"
            >
              Contact
            </a>
          </div>
        </div>
      </nav>
    );
  }
}

export default Navigation;
