import React from "react";
import Layout from "../../common/layouts/Layout";
import SearchFormContainer from "../decorators/SearchFormContainer";
import { Redirect } from "react-router-dom";
import queryString from "query-string";

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchedData: null
    };
  }
  onSearchSubmit = values => {
    this.setState({ searchedData: values });
  };
  buildUrlParamsFromValues = values => {
    const params = {
      perimetreApplicationType: values.type,
      perimetreApplicationCode: values.data.code,
      perimetreApplicationName: values.data.name,
      searchedText: values.text,
      codeDepartement: values.data.codeDepartement,
      codeRegion: values.data.codeRegion
    };
    return queryString.stringify(params);
  };
  render() {
    if (this.state.searchedData) {
      const urlParams = this.buildUrlParamsFromValues(this.state.searchedData);
      return <Redirect push to={`/aides?${urlParams}`} />;
    }
    return (
      <Layout>
        <section className="section container">
          <div className="has-text-centered">
            <h2 className="title is-2">
              Je veux connaître les aides disponibles sur mon territoire.
            </h2>
            <h2 className="title is-3">Où est situé votre projet ?</h2>
            <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
          </div>
        </section>
      </Layout>
    );
  }
}

export default SearchPage;
