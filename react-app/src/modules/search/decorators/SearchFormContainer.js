import React from "react";
import SearchForm from "../presentationals/SearchForm";
import { isPostalCode } from "../../../services/searchLib";
import PropTypes from "prop-types";
import {
  getCommunesFromPostalCode,
  getCommunesFromName,
  getDepartementsByName,
  getRegionsByName
} from "services/geoApi";

const SUGGESTIONS_LIMIT = 5;

class SearchFormContainer extends React.Component {
  static propTypes = {
    onSearchSubmit: PropTypes.string.isRequired
  };
  constructor(props) {
    super(props);
    this.state = {
      suggestions: [],
      text: ""
    };
  }
  static propTypes = {
    onSearchSubmit: PropTypes.func.isRequired,
    text: PropTypes.string
  };
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
          const suggestions = communes.map(function(commune) {
            return {
              text: `${commune.nom} - (commune)`,
              type: "commune",
              data: commune
            };
          });
          return suggestions.slice(0, SUGGESTIONS_LIMIT);
        })
      );
    }
    if (text.length > 1) {
      // communes
      promises.push(
        getCommunesFromName(text).then(result => {
          const communes = result.data;
          const suggestions = communes.map(function(commune) {
            return {
              text: `${commune.nom} (commune)`,
              type: "commune",
              data: commune
            };
          });
          return suggestions.slice(0, SUGGESTIONS_LIMIT);
        })
      );
      // départements
      promises.push(
        getDepartementsByName(text).then(result => {
          const departements = result.data;
          const suggestions = departements.map(function(departement) {
            return {
              text: `${departement.nom} (département)`,
              type: "departement",
              data: departement
            };
          });
          return suggestions.slice(0, SUGGESTIONS_LIMIT);
        })
      );
      // régions
      promises.push(
        getRegionsByName(text).then(result => {
          const regions = result.data;
          const suggestions = regions.map(function(region) {
            return {
              text: `${region.nom} (Région)`,
              type: "region",
              data: region
            };
          });
          return suggestions.slice(0, SUGGESTIONS_LIMIT);
        })
      );
    }
    // when all promises have run, add suggestions to state
    Promise.all(promises).then(promisesResults => {
      let suggestions = [];
      // eslint-disable-next-line
      promisesResults.map(function(result) {
        suggestions = [...suggestions, ...result];
      });
      this.resetSuggestions();
      this.addSuggestions(suggestions);
    });
  };
  onSearchSubmit = values => {
    this.resetSuggestions();
    this.props.onSearchSubmit(values);
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
          text={this.state.text}
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
