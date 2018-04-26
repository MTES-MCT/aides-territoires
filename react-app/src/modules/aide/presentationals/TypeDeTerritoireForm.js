import React from "react";
import { connect } from "react-redux";
import { Field, reduxForm, change, formValues } from "redux-form";
import Store from "store";
import Text from "modules/form/presentationals/Text";
import TextArea from "modules/form/presentationals/TextArea";
import CheckboxGroup from "modules/form/presentationals/CheckboxGroup";
import SubmitButton from "modules/form/presentationals/SubmitButton";

const formName = "typeDeTerritoire";

let TypeDeTerritoireForm = props => {
  return (
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
      <SubmitButton className="is-large is-primary" value="Envoyer" />
      <br />
      <br />
      <pre>{JSON.stringify(props.formValues, null, 2)}</pre>
    </form>
  );
};

const validate = values => {
  const errors = {};
  if (!values.name.trim()) {
    errors.name = "Le champ nom est requis";
  }
  return errors;
};

TypeDeTerritoireForm = reduxForm({
  // a unique name for the form
  form: formName,
  validate,
  initialValues: {
    name: "",
    description: ""
  }
})(TypeDeTerritoireForm);

// map formValues to state
export default connect(state => ({
  formValues: state.form[formName] ? state.form[formName].values : {}
}))(TypeDeTerritoireForm);
