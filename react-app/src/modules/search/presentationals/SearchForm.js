import React from "react";
import PropTypes from "prop-types";
import SearchFormSuggestionList from "../presentationals/SearchFormSuggestionList";

class SearchForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // value of search textfield
      text: props.text ? props.text : ""
    };
  }
  onInputChange = event => {
    const value = event.target.value;
    this.setState({
      text: value
    });
    this.props.onSearchChange(value);
  };
  onSuggestionClick = suggestionData => {
    // on met à jour le contenu du champ de recherche avec le text de la suggestion.
    // on laisse le composant parent gérer le reste concernant la suggestion choisie
    this.setState({
      text: suggestionData.texte
    });
    this.props.onSuggestionClick(suggestionData);
  };
  onSubmit = event => {
    event.preventDefault();
    // transmettre l'évènement de soumission au parent avec le text brut de recherche
    this.props.onSearchSubmit(this.state.text);
  };
  onNewRequest = value => {};
  render() {
    return (
      <div className="search-form">
        <form onSubmit={this.onSubmit}>
          <div className="field has-addons">
            <div className="control is-expanded">
              <input
                onChange={this.onInputChange}
                className="input is-large"
                type="text"
                value={this.state.text}
                placeholder="Entrez un code postal, une ville, un département ou une région"
              />
              {this.props.suggestions.length > 0 && (
                <div className="suggestions">
                  <SearchFormSuggestionList
                    onSuggestionClick={this.onSuggestionClick}
                    suggestions={this.props.suggestions}
                  />
                </div>
              )}
            </div>

            <div className="control">
              <input
                type="submit"
                value="Chercher"
                className="button is-info is-large"
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}

SearchForm.propTypes = {
  onSearchSubmit: PropTypes.func.isRequired,
  onSearchChange: PropTypes.func.isRequired,
  suggestions: PropTypes.array,
  onSuggestionClick: PropTypes.func.isRequired
};

export default SearchForm;
