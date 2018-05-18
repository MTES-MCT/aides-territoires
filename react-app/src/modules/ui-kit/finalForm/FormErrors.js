import React from "react";

const FormErrors = ({ errors }) => {
  const keys = Object.keys(errors);
  return (
    keys.length > 0 && (
      <div className="help is-danger">
        Des erreurs ont été détectées dans le formulaire:
        <ul>{keys.map(key => <li key={key}>{errors[key]}</li>)}</ul>
        <br />
        <br />
      </div>
    )
  );
};

export default FormErrors;
