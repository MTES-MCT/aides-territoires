import React from "react";
import { connect } from "react-redux";
import { Field, reduxForm, getFormValues } from "redux-form";
import store from "../../../store/index";
import {
  TextField,
  TextArea,
  SubmitButton,
  Select,
  CheckboxGroup
} from "modules/bulma/presentationals/Form";
import {
  getCommunesFromPostalCode,
  getCommunesFromName,
  getDepartementsByName,
  getRegionsByName
} from "../../../services/geoApi";

const TYPES_DE_TERRITOIRES_OPTIONS = [
  { value: "europe", label: "Europe" },
  { value: "national", label: "National" },
  { value: "commune", label: "Commune" },
  { value: "departement", label: "Département" },
  { value: "region", label: "Région" },
  { value: "bassin", label: "Bassin" }
];

let AideForm = props => {
  return (
    <form onSubmit={props.handleSubmit}>
      <Field
        className="is-large"
        name="name"
        component={TextField}
        label="Nom de l'aide"
      />
      <Field
        name="description"
        component={TextArea}
        label="Descriptif de l'aide"
      />
      <Field
        name="structurePorteuse"
        className="is-large"
        component={TextField}
        label="Structure porteuse"
      />
      <CheckboxGroup
        name="typesDeTerritoires"
        options={TYPES_DE_TERRITOIRES_OPTIONS}
      />
      {/*
      <Field
        name="typeDeTerritoire"
        component={Select}
        className="is-medium is-multiple is-primary"
        options={TYPES_DE_TERRITOIRES_OPTIONS}
      />
      <br />
    */}
      <pre>{JSON.stringify(props.formValues)}</pre>
      {props.formValues.typeDeTerritoire &&
        props.formValues.typeDeTerritoire.includes("departement") && (
          <Field
            name="codeDepartement"
            label="Précisez le département"
            component={TextField}
            className="is-large"
            autocompleteCallback={getCommunesFromName}
            options={TYPES_DE_TERRITOIRES_OPTIONS}
          />
        )}
      <SubmitButton className="is-large is-primary" value="Envoyer" />
    </form>
  );
};

const formName = "aide";
const validate = values => {
  const errors = {};
  if (!values.name.trim()) {
    errors.name = "Le champ nom est requis";
  }
  if (!values.codeDepartement.trim()) {
    errors.codeDepartement = "Le champ codeDepartement est requis";
  }
  return errors;
};

AideForm = reduxForm({
  // a unique name for the form
  form: formName,
  validate,
  initialValues: {
    name: "",
    description: "",
    structurePorteuse: "",
    typeDeTerritoire: ["region"],
    codeDepartement: ""
  }
})(AideForm);

// map formValues to state
export default connect(state => ({
  formValues: state.form[formName] ? state.form[formName].values : {}
}))(AideForm);
