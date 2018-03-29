import React from "react";

export default class SectionPorteurAideDescription extends React.Component {
  render() {
    return (
      <section id="description" className="section">
        <div className="container">
          <div className="text">
            <p>
              Aides-territoires propose aux porteurs de projets de quartiers
              durables un service leur permettant d'identifier les aides
              mobilisables quelles qu'en soient la forme (financement,
              ingénierie, y compris les appels à projets et manifestation
              d'intérêt), en fonction de leur territoire et de l'état
              d'avancement de leur projet.{" "}
            </p>
            <p>
              <strong>
                Vous portez une telle aide ? Référencez-la en moins de 10
                minutes et elle sera visible par vos cibles potentielles
                utilisant le service Aides-territoires.
              </strong>
              <br />
              <br />
            </p>
          </div>
          <div className="has-text-centered">
            <a
              href="https://goo.gl/forms/lVd7CcukMQU7Ral82"
              className="button is-primary is-large"
            >
              Déposez votre aide
            </a>
          </div>
        </div>
      </section>
    );
  }
}
