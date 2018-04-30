import React from "react";
import Layout from "../../common/layouts/Layout";
import SearchResultList from "modules/search/presentationals/SearchResultList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import queryString from "query-string";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "modules/ui-kit/AppLoader";
import "./SearchResultsPage.css";

const SearchResultsPage = class extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (!this.props.data.aides) {
      return <AppLoader />;
    }
    return (
      <Layout>
        <div className="SearchResultsPage container">
          <div className="columns">
            <div className="column is-one-quarter">
              <SearchFilters />
            </div>
            <div className="column">
              <SearchResultList aides={this.props.data.aides} />
            </div>
          </div>
        </div>
      </Layout>
    );
  }
};

const searchAidesQuery = gql`
  query searchAidesQuery {
    aides: allAides {
      id
      createdAt
      updatedAt
      name
      description
      perimetreApplicationType
      perimetreApplicationName
      perimetreApplicationCode
      perimetreDiffusionType
      etape
      structurePorteuse
      status
    }
  }
`;

export default compose(graphql(searchAidesQuery))(SearchResultsPage);
