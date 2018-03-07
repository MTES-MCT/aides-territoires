import React from "react";
import PropTypes from "prop-types";
import SearchForm from "../../presentationals/searchForm/SearchForm";
import { isPostalCode } from "../../../lib/searchLib";
import { getCommunesFromPostalCode } from "../../../api/searchApi";

function WithSuggestions(SearchForm) {
  return class extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        suggestions: []
      };
    }
    onSearchChange = text => {
      this.resetSuggestions();
      if (isPostalCode(text)) {
        getCommunesFromPostalCode(text).then(result => {
          const communes = result.data;
          communes.map(commune =>
            this.addSuggestion(`${commune.nom} (${commune.code})`)
          );
        });
      }
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
            onSearchSubmit={this.props.onSearchSubmit}
            onSearchChange={this.onSearchChange}
          />
        </div>
      );
    }
  };
}

this.PropTypes = {
  onSearchSubmit: PropTypes.array.isRequired
};

export default WithSuggestions;
