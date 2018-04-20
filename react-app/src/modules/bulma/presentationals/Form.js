import React, { Component } from "react";
import classNames from "classnames";
import PropTypes from "prop-types";
import { Field } from "redux-form";

export const TextField = class extends React.Component {
  constructor(props) {
    super(props);
  }

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
      className,
      ...custom
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
};

export const TextArea = ({
  input,
  label,
  meta: { touched, error },
  className,
  ...custom
}) => {
  return (
    <div className="field">
      <label className="label">{label}</label>
      <textarea className={classNames("textarea", className)} {...input} />
      {error && touched && <div className="help is-danger">{error}</div>}
    </div>
  );
};

export const SubmitButton = props => {
  return (
    <div className="field">
      <input
        className={classNames("button", props.className)}
        type="submit"
        value={props.value}
        disabled={props.disabled}
      />
    </div>
  );
};

export class Select extends Component {
  render() {
    const classes = classNames("select", this.props.className);
    const attributes = {};
    // ajout de l'attribut multiple sur le select
    // si la classe is-multiple est présente
    if (this.props.className.indexOf("is-multiple") !== -1) {
      attributes.multiple = true;
    }
    return (
      <div className="field">
        <div className="control">
          <div className={classNames("select", this.props.className)}>
            <select {...attributes} {...this.props.input}>
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

export class CheckboxGroup extends Component {
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
        <div className="checkboxes">
          <label className="checkbox" key={`checkbox-${index}`}>
            <input
              type="checkbox"
              name={`${name}[${index}]`}
              value={value}
              checked={checked}
              onChange={handleChange}
              onFocus={onFocus}
            />
            {label}
          </label>
        </div>
      );
    });

    return (
      <div>
        <div>{checkboxes}</div>
        {touched && error && <p className="error">{error}</p>}
      </div>
    );
  };

  render() {
    return <Field {...this.props} type="checkbox" component={this.field} />;
  }
}
