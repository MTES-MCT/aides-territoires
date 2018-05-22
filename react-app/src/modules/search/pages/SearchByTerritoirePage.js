import React from "react";
import Layout from "../../common/layouts/Layout";
import SearchFormContainer from "../decorators/SearchFormContainer";
import { Redirect } from "react-router-dom";
import queryString from "query-string";
import classnames from "classnames";
import injectSheet from "react-jss";

const styles = {
  title: {
    paddingBottom: "3rem"
  }
};

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
            <h2 className={classnames("title is-2", this.props.classes.title)}>
              Je veux connaître les aides disponibles sur mon territoire :
            </h2>
            <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
          </div>
        </section>
      </Layout>
    );
  }
}

export default injectSheet(styles)(SearchPage);
