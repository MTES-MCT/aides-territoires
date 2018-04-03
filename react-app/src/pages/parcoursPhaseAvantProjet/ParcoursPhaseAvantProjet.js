import React from "react";
import DefaultLayout from "../../layouts/defaultLayout/DefaultLayout";
import SearchFormContainer from "../../containers/searchFormContainer/SearchFormContainer";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";

class ParcoursPhaseAvantProjet extends React.Component {
  onSearchSubmit = value => {
    console.log(value);
  };
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section has-text-centered">
            <h2 className="title is-2">AVANT PROJET</h2>
            <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
            <Link to="/parcours/phase/avant-projet">
              <RaisedButton label="Suivant" primary={true} />
            </Link>
          </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursPhaseAvantProjet;
