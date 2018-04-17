import React from "react";
import { Field, reduxForm } from "redux-form";
import {
  TextField,
  TextArea,
  SubmitButton
} from "../../bulma/presentationals/Form";

let AideForm = props => {
  return (
    <form onSubmit={props.handleSubmit}>
      <Field
        name="name"
        component={TextField}
        label="Bonjour, comment t'appelles tu ?"
      />
      <Field
        name="howAreYou"
        component={TextField}
        label="Enchanté ! Comment vas tu aujourd'hui ?"
      />
      <Field
        name="email"
        component={TextField}
        label="Une adresse email pour qu'on puisse te recontacter ?"
      />
      <Field name="message" component={TextArea} label="ton message" />
      <Field
        name="phone"
        component={TextField}
        label="Tu peux nous laisser ton téléphone si tu veux"
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
  if (!values.email.trim()) {
    errors.email = "Oups, tu as oublié de nous laisser ton email";
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = "L'adresse email est invalide";
  }
  if (!values.message.trim()) {
    errors.message = "Le champ message est vide";
  }
  return errors;
};

AideForm = reduxForm({
  // a unique name for the form
  form: "contact",
  validate,
  initialValues: {
    name: "",
    howAreYou: "",
    message: "",
    email: "",
    phone: ""
  }
})(AideForm);

export default AideForm;
