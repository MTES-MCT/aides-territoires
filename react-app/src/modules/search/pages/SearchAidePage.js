import React from "react";
import Layout from "../../common/layouts/Layout";
import AideList from "modules/search/presentationals/AideList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import SearchFormContainer from "modules/search/decorators/SearchFormContainer";
import AidesProvider from "modules/search/decorators/AidesProvider";
import queryString from "query-string";
import "./SearchAidePage.css";

const Aides = AidesProvider(AideList);

const SearchAidePage = class extends React.Component {
  state = {};
  constructor(props) {
    super(props);
  }
  buildUrlParamsFromValues = values => {
    const params = {
      perimetreApplicationType: values.type,
      perimetreApplicationCode: values.data.code
    };
    return queryString.stringify(params);
  };
  handlFiltersChange = newValues => {
    this.setState({
      ...newValues.values
    });
    console.log(this.state);
  };
  handleSearchSubmit = values => {
    console.log(this.props);
    const urlParams = queryString.stringify(this.state);
    this.props.history.replace(`${this.props.match.url}?${urlParams}`);
  };
  render() {
    return (
      <Layout>
        <div className="SearchResultsPage container">
          <div className="section">
            <SearchFormContainer onSearchSubmit={this.handleSearchSubmit} />
          </div>
          <div className="columns">
            <div className="column is-one-quarter">
              <SearchFilters onFiltersChange={this.handlFiltersChange} />
            </div>
            <div className="column">
              <Aides
                statusPublication={["published"]}
                perimetreApplicationType={""}
                perimetreApplicationCode={"44109"}
                etape={this.state.etape}
                type={this.state.type}
              />
            </div>
          </div>
        </div>
      </Layout>
    );
  }
};

export default SearchAidePage;
