import React from "react";

export const TextField = ({
  input,
  label,
  meta: { touched, error },
  ...custom
}) => {
  return (
    <div className="field">
      <label className="label">{label}</label>
      <input type="textfield" className="input" {...input} />
      {error && touched && <div className="help is-danger">{error}</div>}
    </div>
  );
};

export const TextArea = ({
  input,
  label,
  meta: { touched, error },
  ...custom
}) => {
  return (
    <div className="field">
      <label className="label">{label}</label>
      <textarea className="textarea" {...input} />
      {error && touched && <div className="help is-danger">{error}</div>}
    </div>
  );
};

export const SubmitButton = props => {
  return (
    <div className="field">
      <input
        className="button is-primary"
        type="submit"
        value={props.value}
        disabled={props.disabled}
      />
    </div>
  );
};
