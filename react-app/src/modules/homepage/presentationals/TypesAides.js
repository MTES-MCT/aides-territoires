import React from "react";

export default class SectionTypeAides extends React.Component {
  render() {
    return (
      <section id="types-aides" className="section">
        <div className="container">
          <p className="text">
            Quelque soit le stade d'avancement de votre projet d'ÉcoQuartier,
            Aides-territoires vous permet d'identifier les aides pertinentes:
          </p>
          <div className="content ">
            <div className="columns">
              <div className="column">
                <div className="aides-icon">
                  <img src="/static/images/icon-compas.png" />
                </div>
                <h2 className="title is-4">Ingénierie</h2>
              </div>
              <div className="column">
                <div className="aides-icon">
                  <img src="/static/images/icon-financement.png" />
                </div>
                <h2 className="title is-4">Financement</h2>
              </div>
              <div className="column">
                <div className="aides-icon">
                  <img src="/static/images/icon-journal.png" />
                </div>
                <h2 className="title is-4">Appels à projet</h2>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}
