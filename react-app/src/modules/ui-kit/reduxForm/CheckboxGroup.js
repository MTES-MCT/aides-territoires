import React, { Component } from "react";
import PropTypes from "prop-types";
import { Field } from "redux-form";
import Checkbox from "material-ui/Checkbox";
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
        <div key={index} style={styles.checkbox}>
          <Checkbox
            label={label}
            name={`${name}[${index}]`}
            checked={checked}
            onCheck={handleChange}
            onFocus={onFocus}
          />
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

const styles = {
  checkbox: {
    display: "block",
    marginBottom: "1rem"
  }
};
