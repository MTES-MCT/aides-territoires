import React from "react";

export default class HeaderPorteurAide extends React.Component {
  render() {
    return (
      <section id="aides-territoires" className="hero">
        <header className="header">
          <div className="header-overlay">
            <div className="hero-body">
              <div className="container">
                <h1 className="title">{this.props.data.titreduheader}</h1>
                <h2 className="subtitle">
                  <div
                    dangerouslySetInnerHTML={{
                      __html: this.props.data.texteduheader
                    }}
                  />
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
