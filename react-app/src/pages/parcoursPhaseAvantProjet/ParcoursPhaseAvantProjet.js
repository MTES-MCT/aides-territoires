import React from "react";
import DefaultLayout from "../../layouts/defaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";

const style = {
  margin: "12px"
};

class ParcoursPhaseAvantProjet extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section has-text-centered">
            <h2 className="title is-2">Phase d'avant projet</h2>
            <Link style={style} to="/parcours/phase">
              <RaisedButton label="Précédent" secondary={true} />
            </Link>
            <Link style={style} to="/parcours/phase/avant-projet">
              <RaisedButton label="Suivant" primary={true} />
            </Link>
          </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursPhaseAvantProjet;
