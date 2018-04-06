import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";

class ParcoursCriteres extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: ""
    };
  }
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section has-text-centered">
            <h2 className="title is-2">Critères</h2>
            <Link to="/">
              <RaisedButton label="Rechercher" primary={true} />
            </Link>
          </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursCriteres;
