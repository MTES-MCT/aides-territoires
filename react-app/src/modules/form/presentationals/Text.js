import React from "react";
import classNames from "classnames";
import TextSuggestions from "./TextSuggestions";

export default class extends React.Component {
  state = {
    suggestions: [],
    showSuggestions: false
  };
  handleChange = async event => {
    const { value } = event.target;
    this.props.input.onChange(value);
    if (this.props.autocompleteCallback) {
      const response = await this.props.autocompleteCallback(value);
      const suggestions = response.data.map(result => ({
        text: result.nom,
        value: result.code
      }));
      if (suggestions.length > 0) {
        this.setState({
          suggestions,
          showSuggestions: true
        });
      }
    }
  };
  handleClick = suggestion => {
    this.setState({ showSuggestions: false });
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
          {...input}
          onChange={this.handleChange}
        />
        {this.state.showSuggestions && (
          <TextSuggestions
            onClick={this.handleClick}
            suggestions={this.state.suggestions}
          />
        )}
        {error && touched && <div className="help is-danger">{error}</div>}
      </div>
    );
  }
}
