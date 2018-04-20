import React from "react";
import { connect } from "react-redux";
import { Field, reduxForm } from "redux-form";
import Text from "modules/form/presentationals/Text";
import TextArea from "modules/form/presentationals/TextArea";
import CheckboxGroup from "modules/form/presentationals/CheckboxGroup";
import SubmitButton from "modules/form/presentationals/SubmitButton";
import {
  getCommunesFromPostalCode,
  getCommunesFromName,
  getDepartementsByName,
  getRegionsByName
} from "../../../services/geoApi";

const TYPES_DE_TERRITOIRES_OPTIONS = [
  { value: "europe", label: "Europe" },
  { value: "france_entiere", label: "France entière" },
  { value: "outre_mer", label: "France outre Mer" },
  { value: "metropole", label: "France Métropole et Corse" },
  { value: "region", label: "Région" },
  { value: "departement", label: "Département" }
  /*{ value: "epci", label: "epci" },
  { value: "bassin", label: "Bassin" },*/
];

let AideForm = props => {
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
      <Field
        name="structurePorteuse"
        className="is-large"
        component={Text}
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
      {props.formValues.typesDeTerritoires &&
        props.formValues.typesDeTerritoires.includes("departement") && (
          <Field
            name="codeDepartement"
            label="Précisez le département"
            component={Text}
            className="is-large"
            autocompleteCallback={getDepartementsByName}
          />
        )}
      {props.formValues.typesDeTerritoires &&
        props.formValues.typesDeTerritoires.includes("region") && (
          <Field
            name="codeRegion"
            label="Précisez la région"
            component={Text}
            className="is-large"
            autocompleteCallback={getRegionsByName}
          />
        )}
      {props.formValues.typesDeTerritoires &&
        props.formValues.typesDeTerritoires.includes("epci") && (
          <Field
            name="codeEpci"
            label="Précisez l'EPCI"
            component={Text}
            className="is-large"
          />
        )}
      <SubmitButton className="is-large is-primary" value="Envoyer" />
      Debug <br />
      <pre>{JSON.stringify(props.formValues, null, 2)}</pre>
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
