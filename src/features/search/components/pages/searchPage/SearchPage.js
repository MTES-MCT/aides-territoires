import React from "react";
import SearchForm from "../../presentationals/searchForm/SearchForm";
import WithSuggestions from "../../hocs/withSuggestions/WithSuggestions";
import SearchFormContainer from "../../containers/searchFormContainer/SearchFormContainer";

class SearchPage extends React.Component {
  render() {
    return (
      <div className="search-page">
        <SearchFormContainer />
      </div>
    );
  }
}

export default SearchPage;
