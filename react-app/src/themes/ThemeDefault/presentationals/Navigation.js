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
        className="navbar is-fixed-top app-main-menu"
        role="navigation"
        aria-label="main navigation"
      >
        <div className="navbar-brand">
          <Link className="navbar-item" to="/#aides-territoires">
            <img style={{ paddingRight: "20px" }} src="images/logo-gouv.png " />{" "}
            <p className="app-name ">
              <strong>Aides-territoires</strong>
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
            <Link
              className="navbar-item"
              onClick={this.handleLinkClick}
              to="/#aides-territoires"
            >
              Aides-territoires
            </Link>
            <Link
              className="navbar-item"
              to="/#comment-ca-marche"
              onClick={this.handleLinkClick}
            >
              Service
            </Link>
            <Link
              className="navbar-item"
              to="/#inscription"
              onClick={this.handleLinkClick}
            >
              Inscription
            </Link>
            <Link
              className="navbar-item"
              to="/porteurs-aides"
              onClick={this.handleLinkClick}
            >
              Porteurs d'aides
            </Link>
            <Link
              className="navbar-item"
              to="/a-propos"
              onClick={this.handleLinkClick}
            >
              À propos
            </Link>
            <Link
              className="navbar-item"
              to="/#contact"
              onClick={this.handleLinkClick}
            >
              Contact
            </Link>
          </div>
        </div>
      </nav>
    );
  }
}

export default Navigation;
