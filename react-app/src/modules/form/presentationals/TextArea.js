import React from "react";
import classNames from "classnames";

export default ({
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
