import React from "react";
import SearchForm from "../presentationals/SearchForm";
import { isPostalCode } from "../../../services/searchLib";
import { change } from "redux-form";
import { connect } from "react-redux";
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
      selectedSuggestion: null,
      suggestions: [],
      // searchForm textfield value.
      text: props.text ? props.text : ""
    };
  }
  static propTypes = {
    onSearchSubmit: PropTypes.func.isRequired,
    text: PropTypes.string
  };
  handleSuggestionClick = suggestionData => {
    this.setState({ selectedSuggestion: suggestionData });
    this.resetSuggestions();
  };
  handleSearchChange = text => {
    const promises = [];
    // typing a postal code ?
    // suggest communes corresponding to the postal code
    if (isPostalCode(text.replace(" ", ""))) {
      promises.push(
        getCommunesFromPostalCode(text).then(result => {
          const communes = result.data;
          const suggestions = communes.map(function(commune) {
            return {
              text: `${commune.nom} (commune - ${commune.codesPostaux[0]})`,
              perimetreApplicationType: "commune",
              perimetreApplicationCode: commune.code,
              perimetreAdditionalData: commune
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
              text: `${commune.nom} (commune - ${commune.codesPostaux[0]})`,
              perimetreApplicationType: "commune",
              perimetreApplicationCode: commune.code,
              perimetreAdditionalData: commune
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
              perimetreApplicationType: "departement",
              perimetreApplicationCode: departement.code,
              perimetreAdditionalData: departement
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
              perimetreApplicationType: "region",
              perimetreApplicationCode: region.code,
              perimetreAdditionalData: region
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
  handleSearchSubmit = () => {
    this.resetSuggestions();
    this.props.change(
      "searchFilters",
      "perimetreApplicationType",
      this.state.selectedSuggestion.perimetreApplicationType
    );
    this.props.change(
      "searchFilters",
      "perimetreApplicationCode",
      this.state.selectedSuggestion.perimetreApplicationCode
    );
    // @FIXME pas pris en compte par redux-form semble-t-il
    this.props.change(
      "searchFilters",
      "perimetreAdditionalData",
      this.state.selectedSuggestion.perimetreAdditionalData
    );
    this.props.onSearchSubmit(this.state.selectedSuggestion);
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
          onSearchSubmit={this.handleSearchSubmit}
          onSearchChange={this.handleSearchChange}
          onSuggestionClick={this.handleSuggestionClick}
        />
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {};
}

function mapDispatchToProps(dispatch) {
  return {
    change: (form, field, value) => {
      dispatch(change(form, field, value));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(
  SearchFormContainer
);
