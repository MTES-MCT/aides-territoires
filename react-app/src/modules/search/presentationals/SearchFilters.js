import React from "react";
import { Form, Field } from "react-final-form";
import { FormSpy } from "react-final-form";
import propTypes from "prop-types";
import "./SearchFilter.css";

const FORME_DE_DIFFUSION_OPTIONS = [
  {
    value: "subvention",
    label: "Subvention"
  },
  {
    value: "formation",
    label: "Formation"
  },
  {
    value: "bonification_interet",
    label: "Bonification d'intérêt"
  },
  {
    value: "pret",
    label: "prêt"
  },
  {
    value: "avance_recuperable",
    label: "avance récupérable"
  },
  {
    value: "garantie",
    label: "Garantie"
  },
  {
    value: "pret_taux_reduit",
    label: "Prêt à taux réduit"
  },
  {
    value: "investissement_en_capital",
    label: "Investissement en capital"
  },
  {
    value: "avantage_fiscal",
    label: "avantage fiscal"
  },
  {
    value: "fonds_de_retour",
    label: "Fonds de retour"
  },
  {
    value: "ingenierie",
    label: "Ingénierie de projet"
  },
  {
    value: "conseil",
    label: "Conseil"
  },
  {
    value: "accompagnement",
    label: "Accompagnement"
  },
  {
    value: "valorisation",
    label: "Valorisation"
  },
  {
    value: "communication",
    label: "Communication"
  }
];

const TYPE_OPTIONS = [
  { value: "financement", label: "Financement" },
  { value: "ingenierie", label: "Ingénierie" },
  { value: "autre", label: "Autre (valorisation, communication etc)" }
];

const ETAPE_OPTIONS = [
  {
    value: "pre_operationnel",
    label: "Pré-opérationnel (Avant-projet, faisabilité)"
  },
  {
    value: "operationnel",
    label: "Opérationnel (Programmation-conception-réalisation)"
  },
  {
    value: "fonctionnement",
    label: "Fonctionnement (Fonctionnement,Phase de vie)"
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
    value: "societe_civile",
    label: "Société civile"
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

const DESTINATION_OPTIONS = [
  {
    value: "etude",
    label: "Etude"
  },
  {
    value: "investissement",
    label: "Investissement"
  },
  {
    value: "fourniture",
    label: "Fourniture"
  },
  {
    value: "fonctionnement",
    label: "Fonctionnement"
  },
  {
    value: "service",
    label: "Service"
  },
  {
    value: "travaux",
    label: "Travaux"
  }
];

const THEMATIQUES_OPTIONS = [
  {
    value: "amenagement_durable",
    label: "Aménagement Durable"
  },
  {
    value: "developpement_local",
    label: "Développement local"
  },
  {
    value: "infrastructures_reseaux_et_deplacements",
    label: "Infrastructures, réseaux et déplacements"
  },
  {
    value: "solidarite_et_cohesion_sociale",
    label: "Solidarité et Cohésion sociale"
  }
];

const validate = values => {
  const errors = {};
  if (!values.nom || values.nom.trim().length === 0) {
    errors.nom = "Le champ nom est requis";
  }
  return errors;
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
      <div className="SearchFilters">
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
                <label className="label"> Temporalité dans le projet </label>
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
                <label className="label"> Modalité de diffusion </label>
                {FORME_DE_DIFFUSION_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="formeDeDiffusion"
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
                <label className="label"> Thématiques </label>
                {THEMATIQUES_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="thematiques"
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
              {/* ================== */}
              <div className="field">
                <label className="label"> Destination de l'aide </label>
                {DESTINATION_OPTIONS.map(option => {
                  return (
                    <div key={option.value}>
                      <label className="checkbox">
                        <Field
                          name="destination"
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
            </form>
          )}
        />
      </div>
    );
  }
}

export default SearchFilters;
