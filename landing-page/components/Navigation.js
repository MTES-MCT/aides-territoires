import React from "react";

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
          <a className="navbar-item js-scrollTo" href="#aides-territoires">
            <img src="/static/images/logo.png " />
            <p className="app-name ">Aides-territoires</p>
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
