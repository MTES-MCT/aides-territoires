import React from "react";
import PropTypes from "prop-types";
import SearchForm from "./SearchForm";
import { change } from "redux-form";
import { connect } from "react-redux";
import SuggestionList from "../ui/SuggestionList";
import { isPostalCode } from "../../lib/search";
import {
  getCommunesFromPostalCode,
  getCommunesFromName,
  getDepartementsByName,
  getRegionsByName
} from "../../lib/geoApi";
import Dialog from "material-ui/Dialog";
import FlatButton from "material-ui/FlatButton";

const SUGGESTIONS_LIMIT = 5;

// 01 : Guadeloupe
// 02 : Martinique
// 04 : La Réunion
// 06 : Mayotte
const codesGeoAPIOutreMer = ["01", "02", "03", "04", "05", "06"];

class SearchFormContainer extends React.Component {
  state = {
    value: "",
    suggestions: [],
    selectedSuggestion: null,
    selectedSuggestionIndex: 0,
    showModal: false
  };
  // ! FIXME suggestions should be returned by graphQL and not computed here.
  handleSubmitAlert = event => {
    event.preventDefault();
    this.setState({ showModal: true });
  };
  handleSubmit = event => {
    event.preventDefault();
    //this.resetSuggestions();
    if (this.state.selectedSuggestion) {
      this.props.change(
        "searchFilters",
        "texte",
        this.state.selectedSuggestion.label
      );
      if (this.state.selectedSuggestion.value.typePerimetreInitialDeRecherche) {
        this.props.change(
          "searchFilters",
          "typePerimetreInitialDeRecherche",
          this.state.selectedSuggestion.value.typePerimetreInitialDeRecherche
        );
      }
      if (this.state.selectedSuggestion.value.codePerimetreInitialDeRecherche) {
        this.props.change(
          "searchFilters",
          "codePerimetreInitialDeRecherche",
          this.state.selectedSuggestion.value.codePerimetreInitialDeRecherche
        );
      }
    }
    if (this.state.selectedSuggestion) {
      this.props.onSubmit(this.state.selectedSuggestion);
    } else {
      alert(
        "Vous devez sélectionner un territoire depuis la liste déroulante."
      );
    }
  };
  handleChange = event => {
    const text = event.target.value;
    this.setState({ value: text });

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
  handleClickSuggestion = (index, suggestion) => {
    this.setState({
      selectedSuggestionIndex: index,
      selectedSuggestion: suggestion,
      value: suggestion.label
    });
    if (this.props.onClick) {
      this.props.onClick(suggestion);
    }
    this.resetSuggestions();
  };
  handleKeyDown = event => {
    const suggestionsLength = this.state.suggestions.length;
    if (event.key === "Enter") {
      // quand on appuie sur entrée, sélectionner la suggestion actuellement active
      this.setState({
        selectedSuggestion: this.state.suggestions[
          this.state.selectedSuggestionIndex
        ]
      });
    }
    if (event.key === "ArrowDown") {
      let nextIndex = this.state.selectedSuggestionIndex + 1;
      if (nextIndex >= suggestionsLength) {
        nextIndex = suggestionsLength - 1;
      }
      this.setState({
        selectedSuggestionIndex: nextIndex
      });
    }
    if (event.key === "ArrowUp") {
      let prevIndex = this.state.selectedSuggestionIndex - 1;
      if (prevIndex < 0) {
        prevIndex = 0;
      }
      this.setState({
        selectedSuggestionIndex: prevIndex
      });
    }
  };
  render() {
    return (
      <div>
        <Dialog
          title=""
          actions={[
            <FlatButton
              label="J'ai compris"
              primary={true}
              keyboardFocused={true}
              onClick={this.handleSubmit}
            />
          ]}
          modal={false}
          open={this.state.showModal}
          onRequestClose={this.handleClose}
        >
          <div className="has-text-centered">
            La base de données Aides territoires est en construction, toutes les
            aides disponibles ne sont pas encore référencées dans notre outil,
            n'hésitez pas à revenir et à vous inscrire à notre newsletter pour
            vous tenir informés!
          </div>
        </Dialog>
        <SearchForm
          value={this.state.value}
          onSubmit={this.handleSubmitAlert}
          onKeyDown={this.handleKeyDown}
          onChange={this.handleChange}
          placeholder={
            "Entrez un code postal, une ville, un département ou une région"
          }
        />
        <SuggestionList
          selectedSuggestionIndex={this.state.selectedSuggestionIndex}
          onClick={this.handleClickSuggestion}
          suggestions={this.state.suggestions}
        />
      </div>
    );
  }
}

SearchFormContainer.propTypes = {
  onClick: PropTypes.func,
  onSubmit: PropTypes.func
};

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

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SearchFormContainer);
