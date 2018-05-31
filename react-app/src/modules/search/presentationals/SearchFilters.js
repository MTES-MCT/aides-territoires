import React from "react";
import { reduxForm } from "redux-form";
import SlideDown from "modules/ui-kit/reactSpring/SlideDown";
import CheckboxGroup from "modules/ui-kit/reduxForm/CheckboxGroup";
import { ArrowDown, ArrowUp } from "modules/ui-kit/bulma/Icons";
import allEnums from "modules/enums";

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

let SearchFilters = class extends React.Component {
  state = {
    activeFilters: {
      perimetreApplicationType: true,
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
    this.setState({
      activeFilters: newFilters
    });
  };
  render() {
    // const { handleSubmit, pristine, reset, submitting } = props;
    return (
      <form style={styles.searchFilters}>
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

        {/***  CATEGORIE PARTICULIER ***/}
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

/*
SearchFilters = connect(state => {
  return {
    formValues: state.form.searchFilters ? state.form.searchFilters.values : {}
  };
})(SearchFilters);
*/

export default SearchFilters;
