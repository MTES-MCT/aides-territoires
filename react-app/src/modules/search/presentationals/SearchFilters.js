import React from "react";
import { Form, Field } from "react-final-form";
import { FormSpy } from "react-final-form";
import propTypes from "prop-types";

// les périmètres géographiques éligibles pour l'aide

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

const FORME_DE_DIFFUSION_OPTIONS = [
  {
    value: "subvention",
    label: "Subvention"
  },
  {
    value: "ingenierie",
    label: "Ingénierie"
  },
  {
    value: "valorisation",
    label: "Valorisation"
  }
];

/*
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
*/

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
              <label className="label"> Type d'aide </label>
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
            <div className="field">
              <label className="label"> Forme de diffusion </label>
              {FORME_DE_DIFFUSION_OPTIONS.map(option => {
                return (
                  <div key={option.value}>
                    <label className="checkbox">
                      <Field
                        name="formeDeDiffusion"
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
