import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import SearchFormContainer from "../../containers/searchFormContainer/SearchFormContainer";
import { Link } from "react-router-dom";
import RaisedButton from "material-ui/RaisedButton";

class ParcoursTerritoire extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: ""
    };
  }
  onSearchSubmit = value => {
    this.setState({ result: value });
  };
  render() {
    const to = { pathname: "/parcours/results" };
    if (this.state.result) {
      to.search = `territoire[type]=${
        this.state.result.type
      }&territoire[codeInsee]=${this.state.result.data.code}`;
    }
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section has-text-centered">
            <h2 className="title is-2">Où est situé votre projet ?</h2>
            <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
            <Link to={to}>
              <RaisedButton label="Rechercher" primary={true} />
            </Link>
          </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursTerritoire;
