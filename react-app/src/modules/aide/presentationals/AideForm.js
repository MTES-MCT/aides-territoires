import React from "react";
// import { Field, reduxForm, change } from "redux-form";
import { Form, Field } from "react-final-form";
import Text from "modules/form/presentationals/Text";
import TextArea from "modules/form/presentationals/TextArea";
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

const initialValues = {
  description: "",
  structurePorteuse: "",
  territoiresEligibles: [],
  regionName: "",
  departementName: "",
  departement: {
    label: "",
    value: ""
  },
  region: {
    label: "",
    value: ""
  }
};

let AideForm = props => {
  return (
    <Form
      onSubmit={props.onSubmit}
      validate={validate}
      initialValues={initialValues}
      render={({ handleSubmit, reset, submitting, pristine, values }) => (
        <form onSubmit={handleSubmit}>
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
          {TERRITOIRES_ELIGIBLES_OPTIONS.map(option => {
            return (
              <div key={option.value}>
                <label className="checkbox">
                  <Field
                    name="territoiresEligibles"
                    component="input"
                    type="checkbox"
                    value={option.value}
                  />{" "}
                  {option.label}
                </label>
              </div>
            );
          })}
          {values.territoiresEligibles &&
            values.territoiresEligibles.includes("regionale") && (
              <Field
                name="region"
                label="Précisez la région"
                component={Text}
                format={suggestion => suggestion.label}
                className="is-large"
                autocompleteCallback={getRegionsByName}
              />
            )}
          {values.territoiresEligibles &&
            values.territoiresEligibles.includes("departementale") && (
              <Field
                name="departement"
                format={suggestion => suggestion.label}
                label="Précisez le département"
                component={Text}
                className="is-large"
                autocompleteCallback={getDepartementsByName}
              />
            )}
          <button
            type="submit"
            className="button is-large is-primary"
            disabled={submitting || pristine}
          >
            Sauver
          </button>
          <br />
          <br />
          <pre>{JSON.stringify(values, null, 2)}</pre>
        </form>
      )}
    />
  );
};

const validate = values => {
  const errors = {};
  if (!values.name || values.name.trim().length === 0) {
    errors.name = "Le champ nom est requis";
  }
  return errors;
};

export default AideForm;
