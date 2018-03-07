import React from "react";
import SearchForm from "../../presentationals/searchForm/SearchForm";
import { isPostalCode } from "../../../lib/searchLib";
import { getCommunesFromPostalCode } from "../../../api/searchApi";

class SearchFormContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      suggestions: []
    };
  }
  onSearchChange = text => {
    this.resetSuggestions();
    if (isPostalCode(text.replace(" ", ""))) {
      getCommunesFromPostalCode(text).then(result => {
        const communes = result.data;
        communes.map(commune =>
          this.addSuggestion(`${commune.nom} (${commune.code})`)
        );
      });
    }
  };
  onSearchSubmit = values => {
    alert("submitted");
  };
  resetSuggestions() {
    this.setState({
      suggestions: []
    });
  }
  /**
   * @param {string} newSuggestion
   */
  addSuggestion(newSuggestion) {
    this.setState({
      suggestions: [...this.state.suggestions, newSuggestion]
    });
  }
  render() {
    return (
      <div className="search-form-container">
        <SearchForm
          suggestions={this.state.suggestions}
          onSearchSubmit={this.onSearchSubmit}
          onSearchChange={this.onSearchChange}
        />
      </div>
    );
  }
}

export default SearchFormContainer;
