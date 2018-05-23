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
import { change } from "redux-form";
import { connect } from "react-redux";
// import queryString from "qs";

const styles = {
  activeFilters: {
    padding: "1rem",
    background: "white"
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
  handleRequestDelete = (fieldId, filterValue) => {
    console.log(this.props.filters);
    const currentFilters = this.props.filters;
    if (currentFilters[fieldId]) {
      const newFilterValue = currentFilters[fieldId].filter(
        filter => filter !== filterValue
      );
      this.props.change("searchFilters", fieldId, newFilterValue);
    }
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
        <Sticky innerZ={9999} enabled={true}>
          <div
            className={classnames(
              this.props.classes.activeFilters,
              "container"
            )}
          >
            <SearchActiveFilters
              onRequestDelete={this.handleRequestDelete}
              filters={this.props.filters}
            />
          </div>
        </Sticky>
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
    }
  };
}

SearchAidePage = connect(mapStateToProps, mapDispatchToProps)(SearchAidePage);
export default injectSheet(styles)(SearchAidePage);
