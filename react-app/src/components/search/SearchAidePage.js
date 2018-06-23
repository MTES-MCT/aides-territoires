import React from "react";
import Layout from "../layouts/Layout";
import SearchFilters from "./SearchFilters";
import SearchActiveFilters from "./SearchActiveFilters";
import RaisedButton from "material-ui/RaisedButton";
import SearchResults from "./SearchResults";
import Dialog from "material-ui/Dialog";
import FlatButton from "material-ui/FlatButton";
import Sticky from "react-stickynode";
import injectSheet from "react-jss";
import classnames from "classnames";
import SearchAidesQuery from "./SearchAidesQuery";
import { cleanSearchFilters } from "../../lib/search";
import { change, reset } from "redux-form";
import { connect } from "react-redux";

let SearchAidePage = class extends React.Component {
  state = {
    showModal: false
  };
  handleButtonClick = () => {
    this.setState({
      showModal: true
    });
  };
  render() {
    return (
      <Layout>
        <Dialog
          title=""
          actions={[
            <FlatButton
              label="OK"
              primary={true}
              keyboardFocused={true}
              onClick={() => this.setState({ showModal: false })}
            />
          ]}
          modal={false}
          open={this.state.showModal}
          onRequestClose={this.handleClose}
        >
          <div className="has-text-centered">
            Cette fonctionnalité sera bientôt disponible!
          </div>
        </Dialog>
        <div className="container">
          <div className="columns">
            <div
              className="column"
              style={{
                textAlign: "right",
                marginTop: "2rem",
                marginBottom: "2px"
              }}
            >
              <RaisedButton
                style={{ marginRight: "20px" }}
                label="Imprimer mes résultats"
                onClick={this.handleButtonClick}
              />
              <RaisedButton
                style={{ marginRight: "20px" }}
                label="Partager mes résultats"
                onClick={this.handleButtonClick}
              />
              <RaisedButton
                style={{ marginRight: "20px" }}
                label="Etre alerté de nouvelles aides"
                onClick={this.handleButtonClick}
              />
            </div>
          </div>
        </div>
        {/* affichr les filtres actifs si il y en a*/}
        {Object.keys(cleanSearchFilters(this.props.filters)).length > 0 && (
          <Sticky innerZ={9999} enabled={true}>
            <div
              className={classnames(
                this.props.classes.activeFilters,
                "container"
              )}
            >
              <StickyActiveStyles />
              <SearchActiveFilters
                onRequestDelete={this.handleRequestDelete}
                onRequestReset={this.handleRequestReset}
                filters={this.props.filters}
              />
            </div>
          </Sticky>
        )}
        <div
          className={classnames(
            "container",
            this.props.classes.filtersAndResults
          )}
        >
          <div className="columns">
            <div className="column is-one-quarter">
              <SearchFilters
                defaultValues={this.props}
                onFiltersChange={this.handlFiltersChange}
              />
            </div>
            <div className="column">
              {/*<pre>{JSON.stringify(this.props.filters, 0, 2)}</pre>*/}
              <SearchResultsTopText />
              <SearchAidesQuery filters={this.props.filters}>
                {({ results }) => (
                  <div>
                    {
                      <SearchResults
                        filters={this.props.filters}
                        results={results}
                      />
                    }
                  </div>
                )}
              </SearchAidesQuery>
            </div>
          </div>
        </div>
      </Layout>
    );
  }
};

const styles = {
  activeFilters: {
    background: " white",
    paddingBottom: "1rem",
    paddingTop: "1rem"
  },
  filtersAndResults: {
    zIndex: 1
  }
};

const SearchResultsTopText = () => (
  <div className="notification">
    Par défaut, le moteur de recherche présente toutes les aides disponibles sur
    votre territoire.Vous pouvez utiliser les filtres ci-contre pour préciser
    votre recherche et sélectionner vos critères
  </div>
);

/**
 * add a shadow on sticky bar when active
 */
const StickyActiveStyles = () => (
  <style>
    {
      ".sticky-outer-wrapper.active .sticky-inner-wrapper {box-shadow: 0px 0px 40px 0px rgba(0, 0, 0, 0.3);}"
    }
  </style>
);

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

function mapDispatchToProps(dispatch) {
  return {
    change: (form, field, value) => {
      dispatch(change(form, field, value));
    },
    reset: () => dispatch(reset("searchFilters"))
  };
}

SearchAidePage = connect(
  mapStateToProps,
  mapDispatchToProps
)(SearchAidePage);
export default injectSheet(styles)(SearchAidePage);
