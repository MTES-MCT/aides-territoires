import React from "react";
import { connect } from "react-redux";
import { Field, reduxForm, change, formValues } from "redux-form";
import Store from "store";
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

// les périmètres géographiques éligibles pour l'aide
const TERRITOIRES_ELIGIBLES_OPTIONS = [
  { value: "europeene", label: "Europe" },
  { value: "nationale", label: "Nationale (Métropole + outre-mer)" },
  { value: "regionale", label: "Régionale" },
  { value: "outre_mer", label: "Outre Mer" },
  { value: "metropole", label: "France Métropole et Corse" },
  { value: "departementale", label: "Département" }
  /*{ value: "epci", label: "epci" },
  { value: "bassin", label: "Bassin" },*/
];

const formName = "aide";

const onDepartementSuggestionClick = suggestion => {
  Store.dispatch(change(formName, "departement", suggestion));
};

const onRegionSuggestionClick = suggestion => {
  Store.dispatch(change(formName, "region", suggestion));
};

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
        name="territoiresEligibles"
        options={TERRITOIRES_ELIGIBLES_OPTIONS}
      />
      {props.formValues.territoiresEligibles &&
        props.formValues.territoiresEligibles.includes("regionale") && (
          <Field
            name="regionName"
            label="Précisez la région"
            component={Text}
            className="is-large"
            autocompleteCallback={getRegionsByName}
            onSuggestionClick={onRegionSuggestionClick}
          />
        )}
      {props.formValues.territoiresEligibles &&
        props.formValues.territoiresEligibles.includes("departementale") && (
          <Field
            name="departementName"
            label="Précisez le département"
            component={Text}
            className="is-large"
            autocompleteCallback={getDepartementsByName}
            onSuggestionClick={onDepartementSuggestionClick}
          />
        )}
      {props.formValues.territoiresEligibles &&
        props.formValues.territoiresEligibles.includes("epci") && (
          <Field
            name="codeEpci"
            label="Précisez l'EPCI"
            component={Text}
            className="is-large"
          />
        )}
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

AideForm = reduxForm({
  // a unique name for the form
  form: formName,
  validate,
  initialValues: {
    name: "",
    description: "",
    structurePorteuse: "",
    territoiresEligibles: [],
    departementName: "",
    regionName: "",
    departement: {},
    region: {}
  }
})(AideForm);

// map formValues to state
export default connect(state => ({
  formValues: state.form[formName] ? state.form[formName].values : {}
}))(AideForm);
