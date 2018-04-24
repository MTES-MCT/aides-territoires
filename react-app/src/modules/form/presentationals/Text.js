import React from "react";
import classNames from "classnames";
import TextSuggestions from "./TextSuggestions";
import PropTypes from "prop-types";
import { change } from "redux-form";
import Store from "../../../store";

export default class extends React.Component {
  static propTypes = {
    // MUST return an object with "value" and "label"
    autocompleteCallback: PropTypes.func,
    onSuggestionClick: PropTypes.func
  };
  state = {
    suggestions: [],
    value: "",
    showSuggestions: false
  };
  handleInputChange = async event => {
    if (this.props.onSuggestionClick) {
      // si on est en train d'écrire, il n'y a pas de suggestion validée
      this.props.onSuggestionClick({});
    }
    const { value } = event.target;
    this.props.input.onChange(value);
    // call redux-form onChange method ourselves
    // this.props.input.onChange(value);
    if (this.props.autocompleteCallback) {
      const response = await this.props.autocompleteCallback(value);
      if (response !== undefined) {
        const suggestions = response.data.map(result => ({
          label: result.nom,
          value: result.code
        }));
        if (suggestions.length > 0) {
          this.setState({
            suggestions,
            showSuggestions: true
          });
        }
      }
    }
  };
  handleSuggestionClick = suggestion => {
    this.props.input.onChange(suggestion.label);
    this.setState({
      showSuggestions: false
    });
    if (this.props.onSuggestionClick) {
      this.props.onSuggestionClick(suggestion);
    }
  };
  render() {
    const {
      input,
      label,
      meta: { touched, error },
      className
    } = this.props;
    return (
      <div className="field">
        <label className="label">{label}</label>
        <input
          type="textfield"
          className={classNames("input", className)}
          autoComplete={this.state.showSuggestions ? "off" : "on"}
          {...input}
          // override redux-form onChange method
          onChange={this.handleInputChange}
        />
        {this.state.showSuggestions && (
          <TextSuggestions
            onSuggestionClick={this.handleSuggestionClick}
            suggestions={this.state.suggestions}
          />
        )}
        {error && touched && <div className="help is-danger">{error}</div>}
      </div>
    );
  }
}
