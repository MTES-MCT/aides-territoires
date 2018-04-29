import React from "react";
import { Form, Field } from "react-final-form";
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
    value: "trash",
    label: "Corbeille"
  },
  {
    value: "published",
    label: "Publiée"
  }
];

const validate = values => {
  const errors = {};
  if (!values.name || values.name.trim().length === 0) {
    errors.name = "Le champ nom est requis";
  }
  return errors;
};

const defaultValues = {
  description: "",
  structurePorteuse: "",
  perimetreApplicationType: "",
  perimetreApplicationName: "",
  perimetreApplicationCode: "",
  perimetreDiffusionType: "",
  lien: "",
  criteresEligibilite: ""
};

class AideForm extends React.Component {
  state = {
    formValues: [],
    submissionStatus: SUBMISSION_STATUS_NOT_STARTED
  };
  static propTypes = {
    // si une aide est passée en props, on considèrera
    // qu'on est en mode édition
    aide: propTypes.object
  };
  constructor(props) {
    super(props);
  }
  handleSubmit = async values => {
    this.setState({
      submissionStatus: SUBMISSION_STATUS_PENDING
    });
    const aide = { ...values };
    const result = await this.props.saveAide({
      variables: aide,
      // mettre à jour la liste des aides dans l'admin
      refetchQueries: ["adminAllAides"]
    });
    this.setState({
      submissionStatus: SUBMISSION_STATUS_FINISHED
    });
  };
  render() {
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
        render={({ handleSubmit, submitting, pristine, values, form }) => (
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
                  name="lien"
                  className="is-large"
                  component={Text}
                  label="Lien"
                />
                <Field
                  name="structurePorteuse"
                  className="is-large"
                  component={Text}
                  label="Structure porteuse"
                />
                <Field
                  name="criteresEligibilite"
                  component={TextArea}
                  label="Critères d'éligibilité"
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
                            onClick={() => {
                              // reset application name and code
                              form.change("perimetreApplicationName", "");
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
                </div>
                <div className="columns">
                  <div className="column">
                    {values.perimetreApplicationType === "departement" && (
                      <Field
                        name="perimetreApplicationName"
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
                        name="perimetreApplicationName"
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
                  {(values.perimetreApplicationType == "region" ||
                    values.perimetreApplicationType == "departement") && (
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

                <button type="submit" className="button is-large is-primary">
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
  }
}

const saveAide = gql`
  mutation saveAide(
    $id: String
    $name: String!
    $description: String!
    $type: String!
    $perimetreDiffusionType: String!
    $perimetreApplicationType: String!
    $perimetreApplicationName: String
    $perimetreApplicationCode: String!
    $etape: String
    $structurePorteuse: String!
    $status: String!
    $lien: String!
    $criteresEligibilite: String
  ) {
    saveAide(
      id: $id
      name: $name
      description: $description
      type: $type
      perimetreDiffusionType: $perimetreDiffusionType
      perimetreApplicationType: $perimetreApplicationType
      perimetreApplicationName: $perimetreApplicationName
      perimetreApplicationCode: $perimetreApplicationCode
      etape: $etape
      structurePorteuse: $structurePorteuse
      status: $status
      lien: $lien
      criteresEligibilite: $criteresEligibilite
    ) {
      name
    }
  }
`;

export default graphql(saveAide, { name: "saveAide" })(AideForm);
