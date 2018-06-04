import React, { Component } from "react";
import classNames from "classnames";

export default class Select extends Component {
  render() {
    const classes = classNames("select", this.props.className);
    const attributes = {};
    // ajout de l'attribut multiple sur le select
    // si la classe is-multiple est présente
    if (
      this.props.className &&
      this.props.className.indexOf("is-multiple") !== -1
    ) {
      attributes.multiple = true;
    }
    return (
      <div className="field">
        <div className="control">
          <div className={classNames("select", this.props.className)}>
            <select {...classes} {...attributes} {...this.props.input}>
              {this.props.options.map(option => {
                return (
                  <option key={option.label} value={option.value}>
                    {option.label}
                  </option>
                );
              })}
            </select>
          </div>
        </div>
      </div>
    );
  }
}
