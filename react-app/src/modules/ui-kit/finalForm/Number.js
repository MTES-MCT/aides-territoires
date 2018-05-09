import React from "react";
import classNames from "classnames";

export default class extends React.Component {
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
          type="number"
          className={classNames("input", className)}
          {...input}
        />
        {error && touched && <div className="help is-danger">{error}</div>}
      </div>
    );
  }
}
