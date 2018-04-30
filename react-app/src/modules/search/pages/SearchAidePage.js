import React from "react";
import Layout from "../../common/layouts/Layout";
import AideList from "modules/search/presentationals/AideList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import AidesProvider from "modules/aide/decorators/AidesProvider";
import queryString from "query-string";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "modules/ui-kit/AppLoader";
import "./SearchAidePage.css";

const SearchResultListWithData = AidesProvider(AideList);

const SearchResultsPage = class extends React.Component {
  state = {
    perimetreApplicationType: "",
    perimetreApplicationCode: "",
    etape: []
  };
  handlFiltersChange = newValues => {
    this.setState({
      ...newValues.values
    });
  };
  render() {
    return (
      <Layout>
        <div className="SearchResultsPage container">
          <div className="columns">
            <div className="column is-one-quarter">
              <SearchFilters onFiltersChange={this.handlFiltersChange} />
            </div>
            <div className="column">
              <SearchResultListWithData
                perimetreApplicationType={"commune"}
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

export default SearchResultsPage;
