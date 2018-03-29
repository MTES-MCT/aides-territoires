import React from "react";

export default class HeaderPorteurAide extends React.Component {
  render() {
    return (
      <section id="aides-territoires" className="hero">
        <header className="header">
          <div className="header-overlay">
            <div className="hero-body">
              <div className="container">
                <h1 className="title">Porteurs d'aides</h1>
                <h2 className="subtitle">
                  <p>
                    Vous portez des aides publiques ou des appels à projet en
                    faveur de l'aménagement durable ?
                    <br />
                    <br />
                    Diffusez vos dispositifs (financiers,ingénierie,appels à
                    projets), trouvez plus facilement des porteurs de projets
                    éligibles
                  </p>
                </h2>
                {/*
                <div className="button is-large is-primary ">
                  <a
                    className="button-lancez-la-recherche js-scrollTo "
                    href="#description"
                  >
                    En savoir plus
                  </a>
                </div>
                */}
              </div>
            </div>
          </div>
        </header>
      </section>
    );
  }
}
