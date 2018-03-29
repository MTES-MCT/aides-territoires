import React from "react";

export default class Content extends React.Component {
  render() {
    return (
      <section id="description" className="section">
        <div className="container">
          <div className="text">
            <p>
              Aides-territoires est une base de données dynamique qui référence
              les aides à destination des territoires afin de les accompagner
              dans leur recherche à toutes les étapes de leur projet
              d’aménagement durable.
            </p>
            <br />
            <p>
              <strong>
                Notre service est actuellement expérimenté pour les projets de
                quartiers durables{" "}
              </strong>
            </p>
            <br />
          </div>
          <div className="has-text-centered">
            <a
              href="https://goo.gl/forms/lVd7CcukMQU7Ral82"
              className="button is-primary is-large"
            >
              Référencez vos aides compatibles
            </a>
          </div>
          <br />
          <br />
          <p className="text">
            D’autres types de projets arrivent, nous enrichissons notre base de
            données : si vos aides concernent d’autres types de projets,
            contactez-nous et nous reviendrons très vite vers vous pour discuter
            des modalités de diffusion de vos aides !
          </p>
        </div>
      </section>
    );
  }
}
