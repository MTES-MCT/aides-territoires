import React from "react";

class Header extends React.Component {
  render() {
    return (
      <header>
        <section className="hero is-info">
          <div className="hero-body">
            <div className="container">
              <h1 className="title">Aides-territoires</h1>
              <h2 class="subtitle">
                Identifiez en quelques clics toutes les aides disponibles pour
                vos projets de quartiers durables
              </h2>
            </div>
          </div>
        </section>
      </header>
    );
  }
}

export default Header;
