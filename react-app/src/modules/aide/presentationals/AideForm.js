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
const PERIMETRE_APPLICATION_OPTIONS = [
  { value: "europe", label: "Europe" },
  { value: "france", label: "Nationale (Métropole + outre-mer)" },
  { value: "region", label: "Régionale" },
  { value: "outre_mer", label: "Outre Mer" },
  { value: "metropole", label: "France Métropole et Corse" },
  { value: "departement", label: "Département" }
];

const PERIMETRE_DIFFUSION_OPTIONS = PERIMETRE_APPLICATION_OPTIONS;

const TYPE_OPTIONS = [
  { value: "financement", label: "Financement" },
  { value: "ingenierie", label: "Ingénierie" },
  { value: "autre", label: "Autre" }
];

const ETAPE_OPTIONS = [
  { value: "pre-operationnel", label: "Pré-opérationnel" },
  { value: "operationnel", label: "Opérationnel" },
  { value: "fonctionnement", label: "Fonctionnement" }
];

const formName = "aide";

const initialValues = {
  description: "",
  structurePorteuse: "",
  perimetreApplication: [],
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
          <div className="field">
            <label className="label"> Périmètre d'application </label>
            {PERIMETRE_APPLICATION_OPTIONS.map(option => {
              return (
                <div key={option.value}>
                  <label className="checkbox">
                    <Field
                      name="perimetreApplication"
                      component="input"
                      type="checkbox"
                      value={option.value}
                    />{" "}
                    {option.label}
                  </label>
                </div>
              );
            })}
          </div>
          {values.perimetreApplication &&
            values.perimetreApplication.includes("region") && (
              <Field
                name="region"
                label="Précisez la région"
                component={Text}
                format={suggestion => suggestion.label}
                className="is-large"
                autocompleteCallback={getRegionsByName}
              />
            )}
          {values.perimetreApplication &&
            values.perimetreApplication.includes("departement") && (
              <Field
                name="departement"
                format={suggestion => suggestion.label}
                label="Précisez le département"
                component={Text}
                className="is-large"
                autocompleteCallback={getDepartementsByName}
              />
            )}
          <div className="field">
            <label className="label"> Périmètre de diffusion </label>
            {PERIMETRE_DIFFUSION_OPTIONS.map(option => {
              return (
                <div key={option.value}>
                  <label className="checkbox">
                    <Field
                      name="perimetreDiffusion"
                      component="input"
                      type="checkbox"
                      value={option.value}
                    />{" "}
                    {option.label}
                  </label>
                </div>
              );
            })}
          </div>
          <div className="field">
            <label className="label"> Financement </label>
            {TYPE_OPTIONS.map(option => {
              return (
                <div key={option.value}>
                  <label className="checkbox">
                    <Field
                      name="type"
                      component="input"
                      type="checkbox"
                      value={option.value}
                    />{" "}
                    {option.label}
                  </label>
                </div>
              );
            })}
          </div>

          <div className="field">
            <label className="label"> Etape </label>
            {ETAPE_OPTIONS.map(option => {
              return (
                <div key={option.value}>
                  <label className="checkbox">
                    <Field
                      name="etape"
                      component="input"
                      type="checkbox"
                      value={option.value}
                    />{" "}
                    {option.label}
                  </label>
                </div>
              );
            })}
          </div>

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
