import React from "react";
import SearchFormContainer from "../../containers/searchFormContainer/SearchFormContainer";
import SearchResultList from "../../presentationals/searchResultList/SearchResultList";

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchedData: {}
    };
  }
  onSearchSubmit = values => {
    this.setState({ searchedData: values });
  };
  render() {
    return (
      <div className="search-page">
        <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
        <SearchResultList searchedData={this.state.searchedData} />
      </div>
    );
  }
}

export default SearchPage;
