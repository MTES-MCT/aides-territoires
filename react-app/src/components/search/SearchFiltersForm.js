import React from "react";
import { reduxForm, Field, change } from "redux-form";
import { compose } from "react-apollo";
import SlideDown from "../ui/reactSpring/SlideDown";
import CheckboxGroup from "../ui/reduxFormMaterialUI/CheckboxGroup";
import { ArrowDown, ArrowUp } from "../ui/bulma/Icons";
import { connect } from "react-redux";
import moment from "moment";
// import { blue300 } from "material-ui/styles/colors";
// import HelpIcon from "material-ui/svg-icons/action/help";
// import InjectSheet from "react-jss";
import "moment/locale/fr";
import withEnums from "../decorators/withEnums";
moment.locale("fr");

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
    position: "relative",
    paddingBottom: "0.5 rem",
    cursor: "pointer",
    textTransform: "uppercase"
  }
};

/**
 * SearchFiltersForm.
 * Please @see  /src/reducers/searchFiltersReducer
 */
let SearchFiltersForm = class extends React.Component {
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
    const { enums } = this.props;
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

        {/*** TYPE D'AIDE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("type")}
          >
            {this.state.activeFilters.type ? <ArrowUp /> : <ArrowDown />}
            {enums.type.label}
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
            {enums.etape.label}
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
            {enums.formeDeDiffusion.label}
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
            {enums.destination.label}
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
            {enums.thematiques.label}
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
            {enums.categorieParticuliere.label}
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
            {enums.perimetreApplicationType.label}
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
      </form>
    );
  }
};

const DateEcheanceField = class extends React.Component {
  state = {
    month: "",
    year: "",
    date: ""
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
      <div style={{ paddingLeft: "40px" }}>
        <Field
          name="dateEcheanceMonth"
          component={props => {
            return (
              <div className="field">
                {/*<label className="label">Mois</label>*/}
                <div className="control">
                  <div className="select">
                    <select {...props.input}>
                      <option value="">Sélectionnez le mois</option>
                      {moment.months().map((month, index) => (
                        <option value={index} key={month}>
                          {month}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            );
          }}
        />
        <Field
          name="dateEcheanceYear"
          component={props => {
            return (
              <div className="field">
                {/*<label className="label">Année</label>*/}
                <div className="control">
                  <div className="select">
                    <select {...props.input}>
                      <option value="">Sélectionnez l'année</option>
                      {this.yearsArray.map(year => (
                        <option value={year} key={year}>
                          {year}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            );
          }}
        />
      </div>
    );
  }
};

export default compose(
  withEnums(),
  reduxForm({
    // a unique name for the form
    form: "searchFilters"
  })
)(SearchFiltersForm);
