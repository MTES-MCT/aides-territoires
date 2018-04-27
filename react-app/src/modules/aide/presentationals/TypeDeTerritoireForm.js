import React from "react";
import { Form, Field } from "react-final-form";
import Text from "modules/form/presentationals/Text";
import TextArea from "modules/form/presentationals/TextArea";

const initialValues = {
  name: "",
  description: ""
};

const validate = values => {
  const errors = {};
  if (!values.name.trim()) {
    errors.name = "Le champ nom est requis";
  }
  return errors;
};

let TypeDeTerritoireForm = props => {
  return (
    <Form
      onSubmit={props.onSubmit}
      validate={validate}
      initialValues={initialValues}
      render={({ handleSubmit, reset, submitting, pristine, values }) => (
        <form onSubmit={props.handleSubmit}>
          <Field
            className="is-large"
            name="name"
            component={Text}
            label="Nom de l'aide"
          />
          <Field
            name="description"
            component={TextArea}
            label="Descriptif de l'aide"
          />
          <button
            type="submit"
            className="button is-large is-primary"
            disabled={submitting || pristine}
          >
            Sauver
          </button>
          <br />
          <br />
          <pre>{JSON.stringify(props.formValues, null, 2)}</pre>
        </form>
      )}
    />
  );
};

export default TypeDeTerritoireForm;
