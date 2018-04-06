import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";
import Checkbox from "material-ui/Checkbox";
import ActionFavorite from "material-ui/svg-icons/action/favorite";
import ActionFavoriteBorder from "material-ui/svg-icons/action/favorite-border";
import Visibility from "material-ui/svg-icons/action/visibility";
import VisibilityOff from "material-ui/svg-icons/action/visibility-off";

const styles = {
  button: {
    margin: "12px"
  },
  block: {
    maxWidth: 500,
    margin: "auto"
  },
  checkbox: {
    marginBottom: 16
  }
};

class ParcoursPhaseAvantProjet extends React.Component {
  state = {
    checked: false
  };
  updateCheck() {
    this.setState(oldState => {
      return {
        checked: !oldState.checked
      };
    });
  }
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section has-text-centered">
            <h2 className="title is-2">Phase d'avant projet</h2>
            <h2 className="subtitle is-2">
              petit texte de description de l'avant projet xxx
            </h2>
            <div className="section" style={styles.block}>
              <Checkbox label="Maîtrise foncière" style={styles.checkbox} />
              <Checkbox
                label="réalisation diagnostics et études diverses"
                style={styles.checkbox}
              />
              <Checkbox
                label="Aménagement du foncier"
                style={styles.checkbox}
              />
              <Checkbox label="Autre (gouvernance)" style={styles.checkbox} />
            </div>
            <Link style={styles.button} to="/parcours/phase">
              <RaisedButton label="Précédent" secondary={true} />
            </Link>
            <Link style={styles.button} to="/parcours/phase/avant-projet">
              <RaisedButton label="Suivant" primary={true} />
            </Link>
          </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursPhaseAvantProjet;
