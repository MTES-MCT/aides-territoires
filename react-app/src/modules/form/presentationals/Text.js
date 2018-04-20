import React from "react";
import classNames from "classnames";

export default class extends React.Component {
  handleChange = event => {
    const { value } = event.target;
    this.props.input.onChange(value);
    if (this.props.autocompleteCallback) {
      this.props.autocompleteCallback(value).then(r => {
        console.log(r);
        this.setState({
          suggestions: []
        });
      });
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
          {...input}
          onChange={this.handleChange}
        />
        {error && touched && <div className="help is-danger">{error}</div>}
      </div>
    );
  }
}
