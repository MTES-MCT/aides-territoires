import React from "react";
import SearchForm from "../../presentationals/searchForm/SearchForm";
import { isPostalCode } from "../../../lib/searchLib";
import {
  getCommunesFromPostalCode,
  getCommunesFromName
} from "../../../api/searchApi";

const SUGGESTIONS_LIMIT = 5;

class SearchFormContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      suggestions: []
    };
  }
  onSuggestionClick = value => {
    this.resetSuggestions();
  };
  onSearchChange = text => {
    const promises = [];
    // typing a postal code ?
    // suggest communes corresponding to the postal code
    if (isPostalCode(text.replace(" ", ""))) {
      promises.push(
        getCommunesFromPostalCode(text).then(result => {
          const communes = result.data;
          const suggestions = communes.map(commune => {
            return `${commune.nom} - (commune)`;
          });
          return suggestions.slice(0, SUGGESTIONS_LIMIT);
        })
      );
    }
    if (text.length > 1) {
      promises.push(
        getCommunesFromName(text).then(result => {
          const communes = result.data;
          const suggestions = communes.map(commune => {
            return `${commune.nom} (commune)`;
          });
          return suggestions.slice(0, SUGGESTIONS_LIMIT);
        })
      );
    }
    // when all promises have run, add suggestions to state
    Promise.all(promises).then(promisesResults => {
      let suggestions = [];
      promisesResults.map(result => {
        suggestions = [...suggestions, ...result];
      });
      this.resetSuggestions();
      this.addSuggestions(suggestions);
    });
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
   * @param {array} newSuggestions - e.g ["Nantes", "Paris"]
   */
  addSuggestions(newSuggestions) {
    this.setState({
      suggestions: [...this.state.suggestions, ...newSuggestions]
    });
  }
  render() {
    return (
      <div className="search-form-container">
        <SearchForm
          {...this.props}
          suggestions={this.state.suggestions}
          onSearchSubmit={this.onSearchSubmit}
          onSearchChange={this.onSearchChange}
          onSuggestionClick={this.onSuggestionClick}
        />
      </div>
    );
  }
}

export default SearchFormContainer;
