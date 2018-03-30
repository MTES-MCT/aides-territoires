import React from "react";

export default class Header extends React.Component {
  render() {
    console.log(this.props);
    return (
      <section id="aides-territoires" className="hero ">
        <header className="header ">
          <div className="header-overlay ">
            <div className="hero-body ">
              <div className="container ">
                <h1
                  className="title"
                  dangerouslySetInnerHTML={{
                    __html: this.props.data.headertitre
                  }}
                />
                <h2 className="subtitle ">
                  <div
                    dangerouslySetInnerHTML={{ __html: this.props.data.header }}
                  />
                  <p>
                    {/*
                    <strong style={{ color: "white" }}>
                      Identifiez en quelques clics toutes les aides disponibles
                      sur votre territoire pour vos projets d'aménagement
                      durable.
                      <br />
                      <br /> Le service actuellement expérimenté pour les
                      projets de quartiers durables, dont les EcoQuartiers.
                    </strong>
                    */}
                  </p>
                </h2>
                <div className="button is-large is-primary">
                  <a
                    className="button-lancez-la-recherche js-scrollTo "
                    href="#inscription"
                  >
                    {this.props.data.headercalltoaction}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </header>
      </section>
    );
  }
}
