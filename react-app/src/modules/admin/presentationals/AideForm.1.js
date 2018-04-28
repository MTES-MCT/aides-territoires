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

const STATUS_OPTIONS = [
  {
    value: "draft",
    label: "Brouillon"
  },
  {
    value: "review_required",
    label: "A vérifier"
  },
  {
    value: "published",
    label: "Publiée"
  },
  {
    value: "corbeille",
    label: "trash"
  }
];

const formName = "aide";

const defaultValues = {
  description: "",
  structurePorteuse: "",
  perimetreApplication: [],
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
  const initialValues = props.values ? props.values : defaultValues;
  console.log(initialValues);
  return (
    <Form
      onSubmit={props.onSubmit}
      validate={validate}
      initialValues={initialValues}
      render={({ handleSubmit, reset, submitting, pristine, values }) => (
        <form onSubmit={handleSubmit}>
          <div className="columns">
            <div className="column">
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
              <Field
                name="populationMin"
                className="is-large"
                component={Text}
                label="population minimum (nombre d'habitant)"
              />
              <Field
                name="populationMax"
                className="is-large"
                component={Text}
                label="population maximum"
              />
            </div>
          </div>

          <div className="columns">
            <div className="column">
              <div className="field">
                <label className="label"> Périmètre d'application </label>
                {PERIMETRE_APPLICATION_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="perimetreApplication"
                          component="input"
                          type="radio"
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
            </div>
            <div className="column">
              <div className="field">
                <label className="label"> Périmètre de diffusion </label>
                {PERIMETRE_DIFFUSION_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="perimetreDiffusion"
                          component="input"
                          type="radio"
                          value={option.value}
                        />{" "}
                        {option.label}
                      </label>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="columns">
            <div className="column">
              <div className="field">
                <label className="label"> Financement </label>
                {TYPE_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="type"
                          component="input"
                          type="radio"
                          value={option.value}
                        />{" "}
                        {option.label}
                      </label>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="column">
              <div className="field">
                <label className="label"> Etape </label>
                {ETAPE_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="etape"
                          component="input"
                          type="radio"
                          value={option.value}
                        />{" "}
                        {option.label}
                      </label>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          <div className="columns">
            <div className="column">
              <div className="field">
                <label className="label"> Status de publication </label>
                {STATUS_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="status"
                          component="input"
                          type="radio"
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
            </div>
          </div>
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
