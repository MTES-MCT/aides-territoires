import React from "react";
import { reduxForm, Field, change } from "redux-form";
import SlideDown from "modules/ui-kit/reactSpring/SlideDown";
import CheckboxGroup from "modules/ui-kit/reduxForm/CheckboxGroup";
import { ArrowDown, ArrowUp } from "modules/ui-kit/bulma/Icons";
import { connect } from "react-redux";
import allEnums from "modules/enums";
import moment from "moment";
import PropTypes from "prop-types";
import "moment/locale/fr";
moment.locale("fr");

const enums = allEnums.aide;

const styles = {
  searchFilters: {
    background: "rgb(250, 250, 250)"
  },
  filter: {
    marginBottom: "0.5 rem",
    borderBottom: "solid rgb(220, 220, 220) 1px",
    padding: "1rem"
  },
  label: {
    paddingBottom: "0.5 rem",
    cursor: "pointer",
    textTransform: "uppercase"
  }
};

const DateEcheanceField = class extends React.Component {
  state = {
    month: "",
    year: "",
    date: ""
  };
  static propTypes = {
    onChange: PropTypes.func.isRequired
  };
  yearsArray = [
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
    2024,
    2025,
    2026,
    2027,
    2028,
    2029,
    2030
  ];
  render() {
    return (
      <div>
        <Field name="dateEcheanceMonth" component="select">
          <option />
          {moment.months().map((month, index) => (
            <option value={index + 1} key={month}>
              {month}
            </option>
          ))}
        </Field>

        <Field name="dateEcheanceYear" component="select">
          <option />
          {this.yearsArray.map(year => {
            return (
              <option value={year} key={year}>
                {year}
              </option>
            );
          })}
        </Field>
        {/*
        <div className="field">
          <label className="label">Mois</label>
          <div className="control">
            <div className="select">
              <select
                value={this.state.month}
                onChange={this.handleChangeMonth}
              >
                <option>Sélectionnez le mois</option>
                {moment.months().map((month, index) => (
                  <option value={index + 1} key={month}>
                    {month}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="field">
          <label className="label">Année</label>
          <div className="control">
            <div className="select">
              <select value={this.state.year} onChange={this.handleChangeYear}>
                <option>Sélectionnez l'année</option>
                {this.yearsArray.map(year => {
                  return (
                    <option value={year} key={year}>
                      {year}
                    </option>
                  );
                })}
              </select>
            </div>
          </div>
        </div>
        */}
      </div>
    );
  }
};

let SearchFilters = class extends React.Component {
  state = {
    month: "",
    year: "",
    activeFilters: {
      perimetreApplicationType: true,
      dateEcheance: true,
      type: false,
      etape: false,
      formeDeDiffusion: false,
      destination: false,
      thematiques: false
    }
  };
  handleLabelClick = filterId => {
    const newFilters = {
      ...this.state.activeFilters,
      [filterId]: !this.state.activeFilters[filterId]
    };
    // ce sont ne sont pas filtres, juste des champs
    // que l'on combine pour composer "dateEcheance"
    // (qui lui est un vrai champ sur l'entité aide)
    delete newFilters.dateEcheanceMois;
    delete newFilters.dateEcheanceAnnee;
    this.setState({
      activeFilters: newFilters
    });
  };
  render() {
    return (
      <form style={styles.searchFilters}>
        {/***  DATE D'ECHEANCE  ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("dateEcheance")}
          >
            {this.state.activeFilters.dateEcheance ? (
              <ArrowUp />
            ) : (
              <ArrowDown />
            )}
            Date d'échéance
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.dateEcheance}
          >
            <DateEcheanceField onChange={this.handleChangeDateEcheance} />
          </SlideDown>
        </div>

        {/***  PERIMETRE D'APPLICATION  ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("perimetreApplicationType")}
          >
            {this.state.activeFilters.perimetreApplicationType ? (
              <ArrowUp />
            ) : (
              <ArrowDown />
            )}
            Échelle
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.perimetreApplicationType}
          >
            <CheckboxGroup
              name="perimetreApplicationType"
              options={enums.perimetreApplicationType.values}
            />
          </SlideDown>
        </div>

        {/*** TYPE D'AIDE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("type")}
          >
            {this.state.activeFilters.type ? <ArrowUp /> : <ArrowDown />}
            {enums.type.name}
          </label>
          <SlideDown maxHeight={400} show={this.state.activeFilters.type}>
            <CheckboxGroup name="type" options={enums.type.values} />
          </SlideDown>
        </div>

        {/*** ETAPE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("etape")}
          >
            {this.state.activeFilters.etape ? <ArrowUp /> : <ArrowDown />}
            {enums.etape.name}
          </label>
          <SlideDown maxHeight={400} show={this.state.activeFilters.etape}>
            <CheckboxGroup name="etape" options={enums.etape.values} />
          </SlideDown>
        </div>

        {/*** MODALITE DE DIFFUSION ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("formeDeDiffusion")}
          >
            {this.state.activeFilters.formeDeDiffusion ? (
              <ArrowUp />
            ) : (
              <ArrowDown />
            )}
            {enums.formeDeDiffusion.name}
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.formeDeDiffusion}
          >
            <CheckboxGroup
              name="formeDeDiffusion"
              options={enums.formeDeDiffusion.values}
            />
          </SlideDown>
        </div>

        {/*** DESTINATION DE L'AIDE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("destination")}
          >
            {this.state.activeFilters.destination ? <ArrowUp /> : <ArrowDown />}
            {enums.destination.name}
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.destination}
          >
            <CheckboxGroup
              name="destination"
              options={enums.destination.values}
            />
          </SlideDown>
        </div>

        {/***  THEMATIQUES ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("thematiques")}
          >
            {this.state.activeFilters.thematiques ? <ArrowUp /> : <ArrowDown />}
            {enums.thematiques.name}
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.thematiques}
          >
            <CheckboxGroup
              name="thematiques"
              options={enums.thematiques.values}
            />
          </SlideDown>
        </div>

        {/***  CATEGORIE PARTICULIERE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("categorieParticuliere")}
          >
            {this.state.activeFilters.categorieParticuliere ? (
              <ArrowUp />
            ) : (
              <ArrowDown />
            )}
            {enums.categorieParticuliere.name}
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.categorieParticuliere}
          >
            <CheckboxGroup
              name="categorieParticuliere"
              options={enums.categorieParticuliere.values}
            />
          </SlideDown>
        </div>
      </form>
    );
  }
};

/*
const validate = values => {
  const errors = {};
  if (!values.nom || values.nom.trim().length === 0) {
    errors.nom = "Le champ nom est requis";
  }
  return errors;
};
*/
SearchFilters = reduxForm({
  // a unique name for the form
  form: "searchFilters"
})(SearchFilters);

function mapDispatchToProps(dispatch) {
  return {
    change: (form, field, value) => {
      dispatch(change(form, field, value));
    }
  };
}

function mapStateToProps(state) {
  if (state.form.searchFilters && state.form.searchFilters.values) {
    return {
      // les filtres sélectionnés par l'utilisateur pour sa recherche
      // ainsi que les données de périmètre qui ont été enregistré
      // par le moteur de recherche pas territoire
      filters: state.form.searchFilters.values
    };
  }
  // éviter une erreur pour cause de filters undefined
  return { filters: {} };
}

SearchFilters = connect(mapDispatchToProps)(SearchFilters);

export default SearchFilters;
