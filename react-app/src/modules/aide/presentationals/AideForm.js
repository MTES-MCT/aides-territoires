import React from "react";
import { Field, reduxForm } from "redux-form";
import {
  TextField,
  TextArea,
  SubmitButton
} from "modules/bulma/presentationals/Form";

let AideForm = props => {
  return (
    <form onSubmit={props.handleSubmit}>
      <Field name="name" component={TextField} label="Nom de l'aide" />
      <Field
        name="description"
        component={TextArea}
        label="Descriptif de l'aide"
      />
      <Field
        name="structurePorteuse"
        component={TextField}
        label="Structure porteuse"
      />
      <SubmitButton value="Envoyer" disabled={props.submitting} />
    </form>
  );
};

const validate = values => {
  const errors = {};
  if (!values.name.trim()) {
    errors.name = "Le champ nom est requis";
  }
};

AideForm = reduxForm({
  // a unique name for the form
  form: "aide",
  validate,
  initialValues: {
    name: "",
    description: "",
    structurePorteuse: ""
  }
})(AideForm);

export default AideForm;
