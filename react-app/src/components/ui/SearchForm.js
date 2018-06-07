import React from "react";
import PropTypes from "prop-types";

class SearchForm extends React.Component {
  state = {
    value: "",
    prevPropsValue: ""
  };
  handleChange = event => {
    this.setState({ value: event.target.value });
    this.props.onChange(event.target.value);
  };
  handleSubmit = event => {
    event.preventDefault();
    // transmettre l'évènement de soumission au parent avec le text brut de recherche
    this.props.onSubmit(this.state.value);
  };

  static getDerivedStateFromProps(nextProps, prevState) {
    // si une nouvelle valeur pour le champ vient du parent, on la prend
    // si et seulement si elle est différente de la dernière valeur qui a été
    // passée par le parent. Dans tous les autre cas, c'est notre composant
    // et son state local qui garde la main.
    // C'est utile uniquement dans le cas d'un champ autocomplete, ou lors du clic
    // sur une suggestion, on veut "imposer" depuis le parent la valeur du champ
    // text
    if (nextProps.value && nextProps.value !== prevState.prevPropsValue) {
      return {
        ...prevState,
        value: nextProps.value,
        // on enregistre la valeur de la prop pour comparaison ultérieure
        prevPropsValue: nextProps.value
      };
    }
    return {
      ...prevState
    };
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <div className="field has-addons">
            <div className="control is-expanded">
              <input
                onChange={this.handleChange}
                className="input is-large"
                type="text"
                value={this.state.value}
                placeholder={
                  this.props.placeholder ? this.props.placeholder : ""
                }
              />
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
  onSubmit: PropTypes.func,
  value: PropTypes.string,
  placeholder: PropTypes.placeholder,
  onChange: PropTypes.func.isRequired
};

export default SearchForm;
