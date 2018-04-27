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
    showSuggestions: false,
    inputKeyDown: null
  };
  handleInputChange = async event => {
    const { value } = event.target;
    if (this.props.autocompleteCallback) {
      this.props.input.onChange({ label: value, value: "" });
    } else {
      this.props.input.onChange(value);
    }
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
    this.props.input.onChange(suggestion);
    this.setState({
      showSuggestions: false
    });
    if (this.props.onSuggestionClick) {
      this.props.onSuggestionClick(suggestion);
    }
  };
  handleInputKeyDown = e => {
    this.setState({
      inputKeyDown: e.key
    });
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
          onKeyDown={this.handleInputKeyDown}
          type="textfield"
          className={classNames("input", className)}
          // autoComplete={this.props.onSuggestionClick ? "off" : "on"}
          autoComplete="off"
          // override redux-form onChange method
          {...input}
          onChange={this.handleInputChange}
        />
        {this.state.showSuggestions && (
          <TextSuggestions
            inputKeyDown={this.state.inputKeyDown}
            onSuggestionClick={this.handleSuggestionClick}
            suggestions={this.state.suggestions}
          />
        )}
        {error && touched && <div className="help is-danger">{error}</div>}
      </div>
    );
  }
}
