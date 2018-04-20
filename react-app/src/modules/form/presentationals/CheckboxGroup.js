import React, { Component } from "react";
import PropTypes from "prop-types";
import { Field } from "redux-form";
import "./CheckboxGroup.css";

export default class CheckboxGroup extends Component {
  static propTypes = {
    options: PropTypes.arrayOf(
      PropTypes.shape({
        label: PropTypes.string.isRequired,
        value: PropTypes.string.isRequired
      })
    ).isRequired
  };

  field = ({ input, meta, options }) => {
    const { name, onChange, onBlur, onFocus } = input;
    const { touched, error } = meta;
    const inputValue = input.value;

    const checkboxes = options.map(({ label, value }, index) => {
      const handleChange = event => {
        const arr = [...inputValue];
        if (event.target.checked) {
          arr.push(value);
        } else {
          arr.splice(arr.indexOf(value), 1);
        }
        onBlur(arr);
        return onChange(arr);
      };
      const checked = inputValue.includes(value);
      return (
        <div key={index} className="checkbox">
          <label className="label" key={`checkbox-${index}`}>
            <input
              type="checkbox"
              name={`${name}[${index}]`}
              value={value}
              checked={checked}
              onChange={handleChange}
              onFocus={onFocus}
            />
            <span>{label}</span>
          </label>
        </div>
      );
    });

    return (
      <div className="CheckboxGroup">
        <div>{checkboxes}</div>
        {touched && error && <p className="error">{error}</p>}
      </div>
    );
  };

  render() {
    return <Field {...this.props} type="checkbox" component={this.field} />;
  }
}
