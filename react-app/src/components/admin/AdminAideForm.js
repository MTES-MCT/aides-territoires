import React from "react";
import { Form, Field } from "react-final-form";
import { Redirect } from "react-router";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import Text from "../ui/finalFormBulma/Text";
import FormErrors from "../ui/finalFormBulma/FormErrors";
import TextArea from "../ui/finalFormBulma/TextArea";
// import DatePicker from "modules/ui-kit/finalForm/DatePicker";
import Number from "../ui/finalFormBulma/Number";
import moment from "moment";
import { getDepartementsByName, getRegionsByName } from "../../lib/geoApi";
import propTypes from "prop-types";
import GraphQLError from "../ui/GraphQLError";
import allEnums from "../../enums";
import withUser from "../decorators/withUser";
const enums = allEnums.aide;

const SUBMISSION_STATUS_NOT_STARTED = "not_started";
const SUBMISSION_STATUS_PENDING = "pending";
const SUBMISSION_STATUS_FINISHED = "finished";

const validate = values => {
  const errors = {};
  if (!values.nom || values.nom.trim().length === 0) {
    errors.nom = "Le champ nom est requis";
  }
  if (!values.statusPublication) {
    errors.statusPublication = 'Le champ "status de publication" est requis';
  }
  if (!values.status) {
    errors.status = `Le champ "statut de l'aide" est requis`;
  }
  return errors;
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
  // values lors de la création d'une nouvelle aide
  getDefaultValues() {
    return {
      nom: "",
      auteur: this.props.user.id,
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
      formeDeDiffusion: ["subvention"],
      status: "ouvert"
    };
  }
  // le formulaire est pré-remplie soit avec les valeurs par défaut
  // (lors de la création d'une aide), soit avec une aide (édition)
  getInitialValues() {
    let values = {};
    if (this.props.operation === "edition") {
      const { aide } = this.props;
      values = {
        ...aide,
        auteur: aide.auteur && aide.auteur.id ? aide.auteur.id : null
      };
    } else {
      values = this.getDefaultValues();
    }
    return values;
  }

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
  renderAuteur() {
    // si on a une aide et que la clef auteur est bien un objet,
    // on affiche les infos concernant l'utilisateur
    return (
      this.props.aide &&
      this.props.aide.auteur !== null &&
      this.props.aide.auteur === "object" && (
        <div>
          <em>
            Crée par {this.props.aide.auteur.name} -{" "}
            {this.props.aide.auteur.roles.join(",")} -{" "}
            {this.props.aide.auteur.email}
          </em>
        </div>
      )
    );
  }
  render() {
    if (this.state.error) {
      return <GraphQLError error={this.state.error} />;
    }
    if (this.state.submissionStatus === SUBMISSION_STATUS_FINISHED) {
      return <Redirect push to="/aide/list" />;
    }
    return (
      <Form
        onSubmit={this.handleSubmit}
        validate={validate}
        initialValues={this.getInitialValues()}
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
                {this.renderAuteur()}
                <Field
                  disabled={true}
                  className="is-large"
                  name="auteur"
                  component={Text}
                />
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
                  label="Origine de l'aide"
                />
                <Field
                  name="lien"
                  className="is-large"
                  component={Text}
                  label="Lien"
                />
                <Field
                  label="Contact"
                  name="contact"
                  className="is-large"
                  component={Text}
                />
                <Field
                  name="populationMin"
                  className="is-large"
                  component={Number}
                  label="population minimum (nombre d'habitant)"
                />
                <Field
                  name="populationMax"
                  className="is-large"
                  component={Number}
                  label="population maximum"
                />
                <Field
                  name="criteresEligibilite"
                  component={TextArea}
                  label="Critères d'éligibilité"
                />
              </div>
            </div>

            <div className="columns">
              <div className="column">
                <div className="field">
                  <label className="label"> Périmètre d'application </label>
                  {enums.perimetreApplicationType.values.map(option => {
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
                      {/*caché : contient le code identifiant du type de territoire sélectionné*/}
                      <Field
                        style={{ display: "none" }}
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
              {/*
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
                  {values.perimetreDiffusionType === "autre" && (
                    <Field
                      name="perimetreDiffusionTypeAutre"
                      className="is-large"
                      component={Text}
                      label="Autre"
                    />
                  )}
                </div>
              </div>
              */}
            </div>

            <hr />

            <div className="columns">
              <div className="column">
                <div className="field">
                  <label className="label"> Type d'aides </label>
                  {enums.type.values.map(option => {
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
                  <label className="label"> Quand mobiliser l'aide ? </label>
                  {enums.etape.values.map(option => {
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
                  {enums.formeDeDiffusion.values.map(option => {
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
                {values.formeDeDiffusion.includes("subvention") && (
                  <Field
                    name="tauxSubvention"
                    className="is-large"
                    component={Number}
                    label="Taux de subvention"
                  />
                )}
                {values.formeDeDiffusion.includes("autre") && (
                  <Field
                    name="formeDeDiffusionAutre"
                    className="is-large"
                    component={Text}
                    label="Autre"
                  />
                )}
              </div>

              {/* ==== */}
              <div className="column">
                <div className="column">
                  <div className="field">
                    <label className="label"> Public visé </label>
                    {enums.beneficiaires.values.map(option => {
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
                  {enums.destination.values.map(option => {
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
                {values.destination &&
                  values.destination.includes("autre") && (
                    <Field
                      name="destinationAutre"
                      className="is-large"
                      component={Text}
                      label="Autre"
                    />
                  )}
              </div>
              <div className="column">
                <div className="field">
                  <label className="label"> Thématiques </label>
                  {enums.thematiques.values.map(option => {
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
                  <label className="label"> Calendrier </label>
                  {enums.status.values.map(option => {
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
              </div>
              <div className="column">
                <div className="field">
                  <label className="label">Date de début</label>
                  <Field
                    name="dateDebut"
                    // value displayed
                    parse={value => (value ? moment(value).toString() : "")}
                    // value registered
                    format={value =>
                      value ? moment(value).format("Y-MM-DD") : ""
                    }
                    className="date input is-large"
                    component="input"
                    type="date"
                    placeholder="Date"
                  />
                </div>

                <div className="field">
                  <label className="label">Date d'échéance</label>
                  <Field
                    name="dateEcheance"
                    // value displayed
                    parse={value => (value ? moment(value).toString() : "")}
                    // value registered
                    format={value =>
                      value ? moment(value).format("Y-MM-DD") : ""
                    }
                    className="date input is-large"
                    component="input"
                    type="date"
                    placeholder="Date"
                  />
                </div>
              </div>
            </div>
            <hr />

            <div className="columns">
              <div className="column">
                <div className="field">
                  <label className="label"> Catégorie particulière </label>
                  {enums.categorieParticuliere.values.map(option => {
                    return (
                      <div key={option.value}>
                        <label className="checkbox">
                          <Field
                            name="categorieParticuliere"
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
                  <div>
                    <label className="radio">
                      <Field
                        name="demandeTiersPossible"
                        component="input"
                        type="checkbox"
                      />{" "}
                      La demande peut être faite par un tiers pour le compte du
                      porteur de projet
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <hr />
            <div className="columns">
              <div className="column">
                <div className="field">
                  <label className="label"> Statut de publication </label>
                  {enums.statusPublication.values.map(option => {
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
              <div className="column">
                <Field
                  name="motsCles"
                  className="is-large"
                  component={Text}
                  label="Mots clefs (séparés par des virgules)"
                />
              </div>
            </div>
            <FormErrors errors={errors} />
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
    $auteur: String
    $nom: String!
    $description: String!
    $type: String!
    $perimetreDiffusionType: String
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
    $formeDeDiffusionAutre: String
    $perimetreDiffusionTypeAutre: String
    $destination: [saveAideDestination]
    $destinationAutre: String
    $thematiques: [saveAideThematiques]
    $dateEcheance: String
    $dateDebut: String
    $tauxSubvention: String
    $populationMin: Int
    $populationMax: Int
    $contact: String
    $status: [saveAideStatus]
    $categorieParticuliere: [saveAideCategorieParticuliere]
    $demandeTiersPossible: Boolean
    $motsCles: String
  ) {
    saveAide(
      id: $id
      auteur: $auteur
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
      formeDeDiffusionAutre: $formeDeDiffusionAutre
      destination: $destination
      destinationAutre: $destinationAutre
      thematiques: $thematiques
      dateDebut: $dateDebut
      dateEcheance: $dateEcheance
      tauxSubvention: $tauxSubvention
      populationMin: $populationMin
      populationMax: $populationMax
      contact: $contact
      status: $status
      categorieParticuliere: $categorieParticuliere
      demandeTiersPossible: $demandeTiersPossible
      motsCles: $motsCles
    ) {
      nom
    }
  }
`;

export default compose(
  withUser({ mandatory: true }),
  graphql(saveAide, { name: "saveAide" })
)(AideForm);
