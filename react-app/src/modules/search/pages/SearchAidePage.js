import React from "react";
import Layout from "../../common/layouts/Layout";
import AideList from "modules/search/presentationals/AideList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import SearchFormContainer from "modules/search/decorators/SearchFormContainer";
import AidesSearchQuery from "modules/search/decorators/AidesSearchQuery";
import queryString from "query-string";
import "./SearchAidePage.css";

const SearchAidePage = class extends React.Component {
  state = {
    type: [],
    etape: [],
    perimetreApplicationType: []
  };
  constructor(props) {
    super(props);
    const urlParams = queryString.parse(props.location.search);
    this.state = {
      ...urlParams
    };
    console.log(this.state);
  }
  handlFiltersChange = newValues => {
    this.setState({
      ...newValues.values
    });
  };
  handleSearchSubmit = values => {
    const urlParams = queryString.stringify(this.state);
    this.props.history.replace(`${this.props.match.url}?${urlParams}`);
  };
  render() {
    return (
      <Layout>
        <div className="SearchResultsPage container">
          <div className="section">
            <SearchFormContainer
              text={this.state.searchedText}
              onSearchSubmit={this.handleSearchSubmit}
            />
          </div>
          <div className="columns">
            <div className="column is-one-quarter">
              <SearchFilters onFiltersChange={this.handlFiltersChange} />
            </div>
            <div className="column">
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"departement"}
                perimetreApplicationCode={""}
                etape={this.state.etape}
                type={this.state.type}
              >
                {({ aides }) => (
                  <div>
                    {aides.length > 0 && (
                      <h2 className="title is-2">Département</h2>
                    )}
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"region"}
                perimetreApplicationCode={"44109"}
                etape={this.state.etape}
                type={this.state.type}
              >
                {({ aides }) => (
                  <div>
                    {aides.length > 0 && <h2 className="title is-2">Région</h2>}
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"outre_mer"}
                perimetreApplicationCode={""}
                etape={this.state.etape}
                type={this.state.type}
              >
                {({ aides }) => (
                  <div>
                    {aides.length > 0 && (
                      <h2 className="title is-2">Outre mer</h2>
                    )}
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"metropole"}
                perimetreApplicationCode={""}
                etape={this.state.etape}
                type={this.state.type}
              >
                {({ aides }) => (
                  <div>
                    {aides.length > 0 && (
                      <h2 className="title is-2">Métropole</h2>
                    )}
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"france"}
                perimetreApplicationCode={""}
                etape={this.state.etape}
                type={this.state.type}
              >
                {({ aides }) => (
                  <div>
                    {aides.length > 0 && (
                      <h2 className="title is-2">Nationale</h2>
                    )}
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"europe"}
                perimetreApplicationCode={""}
                etape={this.state.etape}
                type={this.state.type}
              >
                {({ aides }) => (
                  <div>
                    {aides.length > 0 && (
                      <h2 className="title is-2">Européennes</h2>
                    )}
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
            </div>
          </div>
        </div>
      </Layout>
    );
  }
};

export default SearchAidePage;
