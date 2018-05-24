import React from "react";
import Layout from "../../common/layouts/Layout";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import SearchActiveFilters from "modules/search/presentationals/SearchActiveFilters";
import RaisedButton from "material-ui/RaisedButton";
import SearchResults from "modules/search/presentationals/SearchResults";
import Dialog from "material-ui/Dialog";
import FlatButton from "material-ui/FlatButton";
import Sticky from "react-stickynode";
import injectSheet from "react-jss";
import classnames from "classnames";
import { change, reset } from "redux-form";
import { connect } from "react-redux";

function filtersAreEmpty(filters) {
  const values = Object.keys(filters).filter(
    filterId => filters[filterId] && filters[filterId].length > 0
  );
  if (values.length === 0) {
    return true;
  }
  return false;
}

// import queryString from "qs";

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

let SearchAidePage = class extends React.Component {
  state = {
    showModal: false
  };
  /*
  constructor(props) {
    super(props);
    const urlParams = queryString.parse(props.location.search);
    this.props = {
      ...urlParams
    };
  }
  */
  // désactiver le filtre cliqué
  handleRequestDelete = (fieldId, filterValue) => {
    const currentFilters = this.props.filters;
    if (currentFilters[fieldId]) {
      let newFilterValue = currentFilters[fieldId].filter(
        filter => filter !== filterValue
      );
      if (newFilterValue.length === 0) {
        newFilterValue = null;
      }
      this.props.change("searchFilters", fieldId, newFilterValue);
    }
  };
  handleRequestReset = () => {
    // remet à zéro le formulaire des filtres de recherche via le store
    this.props.reset();
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
        {filtersAreEmpty(this.props.filters) === false && (
          <Sticky innerZ={9999} enabled={true}>
            <div
              className={classnames(
                this.props.classes.activeFilters,
                "container"
              )}
            >
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
              <SearchResults />
            </div>
          </div>
        </div>
      </Layout>
    );
  }
};

function mapStateToProps(state) {
  if (state.form.searchFilters && state.form.searchFilters.values) {
    return { filters: state.form.searchFilters.values };
  }
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

SearchAidePage = connect(mapStateToProps, mapDispatchToProps)(SearchAidePage);
export default injectSheet(styles)(SearchAidePage);
