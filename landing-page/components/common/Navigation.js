import React from "react";
import Link from "next/link";

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
  render() {
    return (
      <nav
        className="navbar is-fixed-top app-main-menu"
        role="navigation"
        aria-label="main navigation"
      >
        <div className="navbar-brand">
          <Link href="/#aides-territoires">
            <a className="navbar-item js-scrollTo">
              <img
                style={{ paddingRight: "20px" }}
                src="/static/images/logo-gouv.png "
              />{" "}
              <img src="/static/images/logo.png " />
              <p className="app-name ">
                <strong>Aides-territoires</strong>
              </p>
            </a>
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
            <Link href="/#aides-territoires">
              <a className="navbar-item">Aides-territoires</a>
            </Link>
            <Link href="/#comment-ca-marche">
              <a className="navbar-item js-scrollTo">Service</a>
            </Link>
            <Link href="/#inscription">
              <a className="navbar-item js-scrollTo">Inscription</a>
            </Link>
            <Link href="/porteurs-aides">
              <a className="navbar-item js-scrollTo">Porteurs d'aides</a>
            </Link>
            <Link href="/a-propos">
              <a className="navbar-item js-scrollTo">À propos</a>
            </Link>
            <Link href="/#contact">
              <a className="navbar-item">Contact</a>
            </Link>
          </div>
        </div>
      </nav>
    );
  }
}

export default Navigation;
