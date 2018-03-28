import React from "react";

class Navigation extends React.Component {
  render() {
    return (
      <nav
        className="navbar is-fixed-top app-main-menu"
        role="navigation"
        aria-label="main navigation"
      >
        <div className="navbar-brand">
          <a className="navbar-item js-scrollTo" href="#aides-territoires">
            <img src="/static/images/logo.png " />
            <p className="app-name ">Aides-territoires</p>
          </a>
          <div className="navbar-burger" data-target="navMenu ">
            <span />
            <span />
            <span />
          </div>
        </div>
        <div className="navbar-menu" id="navMenu ">
          <div className="navbar-end">
            <a className="navbar-item js-scrollTo" href="/#aides-territoires">
              Aides-territoires
            </a>
            <a className="navbar-item js-scrollTo" href="/#comment-ca-marche">
              Le service
            </a>
            <a className="navbar-item js-scrollTo" href="/#inscription">
              Inscription
            </a>
            <a className="navbar-item js-scrollTo" href="/#contact">
              Contact
            </a>
          </div>
        </div>
      </nav>
    );
  }
}

export default Navigation;
