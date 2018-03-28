import React from "react";

export default class SectionBenefices extends React.Component {
  render() {
    return (
      <section id="benefices" className="section ">
        <div className="container">
          <div className="content ">
            Avec Aides-territoires :
            <ul>
              <li>
                {" "}
                Gagnez du temps dans votre recherche d'aides, de
                l'accompagnement au financement
              </li>
              <li>
                {" "}
                Ne passez plus à côté des aides qui correspondent à votre projet
              </li>
              <li>
                Bénéficiez d'une sélection pertinente à chaque étape de votre
                projet
              </li>
            </ul>
          </div>
        </div>
      </section>
    );
  }
}
