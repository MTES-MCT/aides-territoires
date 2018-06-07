import React from "react";
import PropTypes from "prop-types";
import SearchForm from "./SearchForm";
import SuggestionList from "./SuggestionList";
import { isPostalCode } from "../../lib/search";
import {
  getCommunesFromPostalCode,
  getCommunesFromName,
  getDepartementsByName,
  getRegionsByName
} from "../../lib/geoApi";

const SUGGESTIONS_LIMIT = 5;

// 01 : Guadeloupe
// 02 : Martinique
// 04 : La Réunion
// 06 : Mayotte
const codesGeoAPIOutreMer = ["01", "02", "03", "04", "05", "06"];

class SearchFormAidesTerritoires extends React.Component {
  state = {
    value: "",
    suggestions: [],
    selectedSuggestion: null
  };
  // ! FIXME suggestions should be returned by graphQL and not computed here.
  handleSubmit = suggestion => {
    if (this.props.onSubmit) {
      this.props.onSubmit(this.state.selectedSuggestion);
    }
  };
  handleChange = text => {
    const promises = [];
    // typing a postal code ?
    // suggest communes corresponding to the postal code
    if (isPostalCode(text.replace(" ", ""))) {
      promises.push(
        getCommunesFromPostalCode(text).then(result => {
          const communes = result.data;
          const suggestions = communes.map(function(commune) {
            return {
              label: `${commune.nom} (commune - ${commune.codesPostaux[0]})`,
              value: {
                type: "territoire",
                typePerimetreInitialDeRecherche: "commune",
                codePerimetreInitialDeRecherche: commune.code,
                data: commune
              }
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
              label: `${commune.nom} (commune - ${commune.codesPostaux[0]})`,
              value: {
                type: "territoire",
                typePerimetreInitialDeRecherche: "commune",
                codePerimetreInitialDeRecherche: commune.code,
                data: commune
              }
            };
          });
          return suggestions.slice(0, SUGGESTIONS_LIMIT);
        })
      );
      // départements
      promises.push(
        getDepartementsByName(text).then(result => {
          const departements = result.data;
          const suggestions = [];
          departements.forEach(departement => {
            if (!codesGeoAPIOutreMer.includes(departement.codeRegion)) {
              suggestions.push({
                label: `${departement.nom} (département)`,
                value: {
                  type: "territoire",
                  typePerimetreInitialDeRecherche: "departement",
                  codePerimetreInitialDeRecherche: departement.code,
                  data: departement
                }
              });
            }
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
              label: `${region.nom} (Région)`,
              value: {
                type: "territoire",
                typePerimetreInitialDeRecherche: "region",
                codePerimetreInitialDeRecherche: region.code,
                data: region
              }
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
      // remove existing suggestions
      this.resetSuggestions();
      // add new suggestions
      this.addSuggestions(suggestions);
    });
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
  handleClickSuggestion = suggestion => {
    this.setState({
      selectedSuggestion: suggestion,
      value: suggestion.label
    });
    if (this.props.onClick) {
      this.props.onClick(suggestion);
    }
    this.resetSuggestions();
  };
  render() {
    return (
      <div>
        <SearchForm
          value={this.state.value}
          onSubmit={this.handleSubmit}
          onChange={this.handleChange}
        />
        <SuggestionList
          onClick={this.handleClickSuggestion}
          suggestions={this.state.suggestions}
        />
      </div>
    );
  }
}

SearchFormAidesTerritoires.propTypes = {
  onClick: PropTypes.func,
  onSubmit: PropTypes.func
};

export default SearchFormAidesTerritoires;
