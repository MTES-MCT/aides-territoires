import React from "react";
import Layout from "../../common/layouts/Layout";
import AideList from "modules/search/presentationals/AideList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import AidesProvider from "modules/search/decorators/AidesProvider";
import "./SearchAidePage.css";

const Aides = AidesProvider(AideList);

const SearchResultsPage = class extends React.Component {
  state = {};
  handlFiltersChange = newValues => {
    this.setState({
      ...newValues.values
    });
    console.log(this.state);
    // this.props.history.replace("/foo");
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

export default SearchResultsPage;
