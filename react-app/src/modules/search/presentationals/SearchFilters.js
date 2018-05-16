import React from "react";
import { reduxForm } from "redux-form";
import SlideDown from "modules/ui-kit/reactSpring/SlideDown";
import CheckboxGroup from "modules/ui-kit/reduxForm/CheckboxGroup";
import { connect } from "react-redux";
import { ArrowDown, ArrowUp } from "modules/ui-kit/bulma/Icons";
import {
  PERIMETRE_APPLICATION_OPTIONS,
  PERIMETRE_DIFFUSION_OPTIONS,
  TYPE_OPTIONS,
  ETAPE_OPTIONS,
  FORME_DE_DIFFUSION_OPTIONS,
  BENEFICIAIRES_OPTIONS,
  DESTINATION_OPTIONS,
  THEMATIQUES_OPTIONS,
  STATUS_OPTIONS,
  STATUS_PUBLICATION_OPTIONS
} from "modules/aide/enums";

let SearchFilters = class extends React.Component {
  state = {
    activeFilters: {
      perimetreApplication: true,
      type: true,
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
    const { props } = this;
    const { handleSubmit, pristine, reset, submitting } = props;
    return (
      <form style={styles.searchFilters}>
        {/***  PERIMETRE D'APPLICATION ***/}
        {/*
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("perimetreApplicationType")}
          >
            Périmètre d'application
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.perimetreApplication}
          >
            <CheckboxGroup
              name="perimetreApplicationType"
              options={PERIMETRE_APPLICATION_OPTIONS}
            />
          </SlideDown>
        </div>
        */}
        {/*** TYPE D'AIDE ***/}
        <div style={styles.filter} className="field filter">
          <label
            style={styles.label}
            className="label"
            onClick={() => this.handleLabelClick("type")}
          >
            {this.state.activeFilters.type ? <ArrowUp /> : <ArrowDown />}
            Type d'aide{" "}
          </label>
          <SlideDown maxHeight={400} show={this.state.activeFilters.type}>
            <CheckboxGroup name="type" options={TYPE_OPTIONS} />
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
            Étape
          </label>
          <SlideDown maxHeight={400} show={this.state.activeFilters.etape}>
            <CheckboxGroup name="etape" options={ETAPE_OPTIONS} />
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
            Modalité de diffusion
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.formeDeDiffusion}
          >
            <CheckboxGroup
              name="formeDeDiffusion"
              options={FORME_DE_DIFFUSION_OPTIONS}
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
            Destination
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.destination}
          >
            <CheckboxGroup name="destination" options={DESTINATION_OPTIONS} />
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
            Thématiques
          </label>
          <SlideDown
            maxHeight={400}
            show={this.state.activeFilters.thematiques}
          >
            <CheckboxGroup name="thematiques" options={THEMATIQUES_OPTIONS} />
          </SlideDown>
        </div>
      </form>
    );
  }
};

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

const validate = values => {
  const errors = {};
  if (!values.nom || values.nom.trim().length === 0) {
    errors.nom = "Le champ nom est requis";
  }
  return errors;
};

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
