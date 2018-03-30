import React from "react";
import BulmaCard from "../common/BulmaCard";

export default class Equipe extends React.Component {
  render() {
    return (
      <div id="equipe" className="section container">
        <h2 className="title is-2">L’équipe Aides-territoires</h2>
        <p>
          Aides-territoires, c'est une équipe motivée pour vous proposer un
          outil adapté à vos besoins, que vous recherchiez des aides ou que vous
          en proposiez.{" "}
        </p>
        <br />
        <div className="columns">
          <div className="column">
            <BulmaCard image={"/static/images/elise.jpeg"}>
              <p class="title is-4">Élise, intrapreneuse</p>
              <p class="is-6">
                Ingénieur et urbaniste au Ministère de la Cohésion des
                Territoires, je suis au carrefour des besoins des collectivités,
                des services de l'Etat, des ministères et de leurs opérateurs.
              </p>
            </BulmaCard>
          </div>
          <div className="column">
            <BulmaCard image={"/static/images/yann.jpeg"}>
              <p class="title is-4">Yann, développeur</p>
              <p class="is-6">
                Développeur spécialisé en applications web : React, Node,
                GraphQL, APIs, Vue.js, REST
              </p>
            </BulmaCard>
          </div>
          <div className="column">
            <BulmaCard image={"/static/images/roxane.jpg"}>
              <p class="title is-4">Roxane, coach</p>
              <p class="is-6">Fan d'utilité sociale et d'avocats</p>
            </BulmaCard>
          </div>
        </div>
      </div>
    );
  }
}
