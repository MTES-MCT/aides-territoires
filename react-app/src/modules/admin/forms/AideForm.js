import React from "react";
import { Form, Field } from "react-final-form";
import { Redirect } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import Text from "modules/ui-kit/finalForm/Text";
import TextArea from "modules/ui-kit/finalForm/TextArea";
import DatePicker from "modules/ui-kit/finalForm/DatePicker";
import {
  getDepartementsByName,
  getRegionsByName
} from "../../../services/geoApi";
import propTypes from "prop-types";
import GraphQLError from "../../ui-kit/GraphQLError";

const SUBMISSION_STATUS_NOT_STARTED = "not_started";
const SUBMISSION_STATUS_PENDING = "pending";
const SUBMISSION_STATUS_FINISHED = "finished";

// les périmètres géographiques éligibles pour l'aide
const PERIMETRE_APPLICATION_OPTIONS = [
  { value: "commune", label: "Commune" },
  { value: "departement", label: "Département" },
  { value: "region", label: "Régionale" },
  { value: "metropole", label: "National (hors Outre-mer)" },
  // { value: "outre_mer", label: "Outre Mer" },
  { value: "france", label: "National (métropole + Outre-mer)" },
  { value: "europe", label: "Europe" }
];

// les périmètres géographiques éligibles pour l'aide
const PERIMETRE_DIFFUSION_OPTIONS = [
  { value: "europe", label: "Europe" },
  { value: "metropole", label: "National" },
  { value: "outre_mer", label: "Outre Mer" },
  { value: "region", label: "Régional" },
  { value: "departement", label: "Départemental" },
  { value: "autre", label: "Autre" }
];

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

const defaultValues = {
  nom: "",
  description: "",
  structurePorteuse: "",
  perimetreApplicationType: "france",
  perimetreApplicationNom: "",
  perimetreApplicationCode: "",
  perimetreDiffusionType: "france",
  lien: "",
  criteresEligibilite: "",
  statusPublication: "published",
  type: "financement",
  etape: "pre_operationnel",
  beneficiaires: ["commune"],
  formeDeDiffusion: "subvention"
};

class AideForm extends React.Component {
  state = {
    formValues: [],
    submissionStatus: SUBMISSION_STATUS_NOT_STARTED,
    error: null
  };
  static propTypes = {
    // si une aide est passée en props, on considèrera
    // qu'on est en mode édition
    aide: propTypes.object
  };
  handleSubmit = values => {
    this.setState({
      submissionStatus: SUBMISSION_STATUS_PENDING
    });
    const aide = { ...values };
    this.props
      .saveAide({
        variables: aide,
        // mettre à jour la liste des aides dans l'admin
        refetchQueries: ["adminAllAides"]
      })
      .then(r => {
        this.setState({
          submissionStatus: SUBMISSION_STATUS_FINISHED
        });
      })
      .catch(e => this.setState({ error: e }));
  };
  render() {
    if (this.state.error) {
      return <GraphQLError error={this.state.error} />;
    }
    if (this.state.submissionStatus === SUBMISSION_STATUS_FINISHED) {
      return <Redirect push to="/aide/list" />;
    }
    const initialValues = !this.props.aide
      ? defaultValues
      : Object.assign({}, defaultValues, this.props.aide);
    return (
      <Form
        onSubmit={this.handleSubmit}
        validate={validate}
        initialValues={initialValues}
        render={({
          handleSubmit,
          submitting,
          pristine,
          values,
          errors,
          form
        }) => (
          <form onSubmit={handleSubmit}>
            <div className="columns">
              <div className="column">
                <Field
                  className="is-large"
                  name="nom"
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
                  name="lien"
                  className="is-large"
                  component={Text}
                  label="Lien"
                />
                <Field
                  name="criteresEligibilite"
                  component={TextArea}
                  label="Critères d'éligibilité"
                />
                <Field name="dateEcheance" component={DatePicker} />
                {/*
                <Field
                  name="populationMin"
                  className="is-large"
                  type={Text}
                  label="population minimum (nombre d'habitant)"
                />
                <Field
                  name="populationMax"
                  className="is-large"
                  component={Text}
                  label="population maximum"
                />
                */}
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
                            onClick={() => {
                              // reset application name and code
                              form.change("perimetreApplicationNom", "");
                              form.change("perimetreApplicationCode", "");
                            }}
                            name="perimetreApplicationType"
                            component="input"
                            type="radio"
                            value={option.value}
                          />{" "}
                          {option.label}
                        </label>
                      </div>
                    );
                  })}
                  {errors.perimetreApplicationType}
                </div>
                <div className="columns">
                  <div className="column">
                    {values.perimetreApplicationType === "departement" && (
                      <Field
                        name="perimetreApplicationNom"
                        // format={suggestion => suggestion.label}
                        label="Précisez le département"
                        component={Text}
                        className="is-large"
                        onSuggestionClick={suggestion => {
                          form.change(
                            "perimetreApplicationCode",
                            suggestion.value
                          );
                        }}
                        autocompleteCallback={getDepartementsByName}
                      />
                    )}
                    {values.perimetreApplicationType === "region" && (
                      <Field
                        name="perimetreApplicationNom"
                        label="Précisez la région"
                        component={Text}
                        className="is-large"
                        autocompleteCallback={getRegionsByName}
                        onSuggestionClick={suggestion => {
                          form.change(
                            "perimetreApplicationCode",
                            suggestion.value
                          );
                        }}
                      />
                    )}
                  </div>
                  {(values.perimetreApplicationType === "region" ||
                    values.perimetreApplicationType === "departement") && (
                    <div className="column">
                      <Field
                        name="perimetreApplicationCode"
                        label="code territoire"
                        component={Text}
                        className="is-large"
                        disabled={true}
                        autocompleteCallback={getDepartementsByName}
                      />
                    </div>
                  )}
                </div>
              </div>
              <div className="column">
                <div className="field">
                  <label className="label"> Périmètre de diffusion </label>
                  {PERIMETRE_DIFFUSION_OPTIONS.map(option => {
                    return (
                      <div key={option.value}>
                        <label className="checkbox">
                          <Field
                            name="perimetreDiffusionType"
                            component="input"
                            type="radio"
                            value={option.value}
                          />{" "}
                          {option.label}
                        </label>
                      </div>
                    );
                  })}
                  {/* perimetreDiffusionTypeAutre */}
                  {values.perimetreDiffusionType === "autre" && (
                    <Field
                      name="perimetreDiffusionTypeAutre"
                      className="is-large"
                      component={Text}
                      label="Autre"
                    />
                  )}
                  {/* /perimetreDiffusionTypeAutre*/}
                </div>
              </div>
            </div>

            <hr />

            <div className="columns">
              <div className="column">
                <div className="field">
                  <label className="label"> Type d'aides </label>
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
              </div>
            </div>
            <hr />
            <div className="columns">
              {/* ==== */}
              <div className="column">
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
              </div>
              {/* ==== */}
              <div className="column">
                <div className="column">
                  <div className="field">
                    <label className="label"> Public visé </label>
                    {BENEFICIAIRES_OPTIONS.map(option => {
                      return (
                        <div key={option.value}>
                          <label className="checkbox">
                            <Field
                              name="beneficiaires"
                              component="input"
                              type="checkbox"
                              value={option.value}
                            />{" "}
                            {option.label}
                          </label>
                        </div>
                      );
                    })}
                    {/* perimetreDiffusionTypeAutre */}
                    {values.beneficiaires.includes("autre") && (
                      <Field
                        name="beneficiairesAutre"
                        className="is-large"
                        component={Text}
                        label="Autre"
                      />
                    )}
                    {/* /perimetreDiffusionTypeAutre*/}
                  </div>
                </div>
              </div>
            </div>
            <hr />
            <div className="columns">
              <div className="column">
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
              </div>
              <div className="column">
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
              </div>
            </div>
            <hr />
            <div className="columns">
              <div className="column">
                <div className="field">
                  <label className="label"> Statut de publication </label>
                  {STATUS_OPTIONS.map(option => {
                    return (
                      <div key={option.value}>
                        <label className="checkbox">
                          <Field
                            name="statusPublication"
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

            <button
              disabled={
                this.state.submissionStatus === SUBMISSION_STATUS_PENDING
                  ? true
                  : false
              }
              type="submit"
              className="button is-large is-primary"
            >
              {this.state.submissionStatus === SUBMISSION_STATUS_PENDING
                ? "envoi en cours ..."
                : "Sauver"}
            </button>
            <br />
            <br />
            <pre>{JSON.stringify(values, null, 2)}</pre>
          </form>
        )}
      />
    );
  }
}

const saveAide = gql`
  mutation saveAide(
    $id: String
    $nom: String!
    $description: String!
    $type: String!
    $perimetreDiffusionType: String!
    $perimetreApplicationType: String!
    $perimetreApplicationNom: String
    $perimetreApplicationCode: String!
    $etape: [saveAideEtape]
    $structurePorteuse: String!
    $statusPublication: String!
    $lien: String!
    $criteresEligibilite: String
    $beneficiaires: [saveAideBeneficiaires]
    $beneficiairesAutre: String
    $formeDeDiffusion: [saveAideFormeDeDiffusion]
    $perimetreDiffusionTypeAutre: String
    $destination: [saveAideDestination]
    $thematiques: [saveAideThematiques]
    $dateEcheance: String
  ) {
    saveAide(
      id: $id
      nom: $nom
      description: $description
      type: $type
      perimetreDiffusionType: $perimetreDiffusionType
      perimetreDiffusionTypeAutre: $perimetreDiffusionTypeAutre
      perimetreApplicationType: $perimetreApplicationType
      perimetreApplicationNom: $perimetreApplicationNom
      perimetreApplicationCode: $perimetreApplicationCode
      etape: $etape
      structurePorteuse: $structurePorteuse
      statusPublication: $statusPublication
      lien: $lien
      criteresEligibilite: $criteresEligibilite
      beneficiaires: $beneficiaires
      beneficiairesAutre: $beneficiairesAutre
      formeDeDiffusion: $formeDeDiffusion
      destination: $destination
      thematiques: $thematiques
      dateEcheance: $dateEcheance
    ) {
      nom
    }
  }
`;

export default graphql(saveAide, { name: "saveAide" })(AideForm);
