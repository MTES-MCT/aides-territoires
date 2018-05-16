import React from "react";
import Layout from "../../common/layouts/Layout";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import SearchActiveFilters from "modules/search/presentationals/SearchActiveFilters";
import RaisedButton from "material-ui/RaisedButton";
import SearchResults from "modules/search/presentationals/SearchResults";
import Dialog from "material-ui/Dialog";
import FlatButton from "material-ui/FlatButton";
// import queryString from "qs";
import "./SearchAidePage.css";

const SearchAidePage = class extends React.Component {
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
              style={{ textAlign: "right", marginTop: "2rem" }}
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
        <div className="SearchResultsPage container">
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

export default SearchAidePage;
