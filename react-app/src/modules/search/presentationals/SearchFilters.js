import React from "react";
import { Form, Field } from "react-final-form";
import { FormSpy } from "react-final-form";
import { Redirect } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import Text from "modules/ui-kit/finalForm/Text";
import TextArea from "modules/ui-kit/finalForm/TextArea";
import {
  getDepartementsByName,
  getRegionsByName
} from "../../../services/geoApi";
import propTypes from "prop-types";

const SUBMISSION_STATUS_NOT_STARTED = "not_started";
const SUBMISSION_STATUS_PENDING = "pending";
const SUBMISSION_STATUS_FINISHED = "finished";

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
  {
    value: "pre_operationnel",
    label: "Pré-opérationnel"
  },
  {
    value: "operationnel",
    label: "Opérationnel"
  },
  {
    value: "fonctionnement",
    label: "Fonctionnement"
  }
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
  }
];

const BENEFICIAIRES_OPTIONS = [
  {
    value: "commune",
    label: "Commune"
  },
  {
    value: "EPCI",
    label: "EPCI"
  },
  {
    value: "entreprises",
    label: "Entreprises"
  },
  {
    value: "associations",
    label: "Associations"
  },
  {
    value: "autre",
    label: "Autre"
  }
];

const validate = values => {
  const errors = {};
  if (!values.nom || values.nom.trim().length === 0) {
    errors.nom = "Le champ nom est requis";
  }
  return errors;
};

const defaultValues = {
  nom: ""
};

class SearchFilters extends React.Component {
  static propTypes = {
    // si une aide est passée en props, on considèrera
    // qu'on est en mode édition
    aide: propTypes.object,
    onFiltersChange: propTypes.func
  };
  handleSubmit = values => {};
  handleFormChange = values => {
    this.props.onFiltersChange(values);
  };
  render() {
    return (
      <Form
        onSubmit={this.handleSubmit}
        validate={validate}
        initialValues={defaultValues}
        render={({
          handleSubmit,
          submitting,
          pristine,
          values,
          errors,
          form
        }) => (
          <form onSubmit={handleSubmit}>
            {/* listen for form values change from outside of the <form> tag */}
            <FormSpy
              subscription={{ values: true }}
              onChange={this.handleFormChange}
            />
            {/* ================== */}
            <div className="field">
              <label className="label"> Status de publication </label>
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
            {/* ================== */}
            <div className="field">
              <label className="label"> Etapes </label>
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
            {/* ================== */}

            <br />
            <br />
            <pre>{JSON.stringify(values, null, 2)}</pre>
          </form>
        )}
      />
    );
  }
}

export default SearchFilters;
