import React from "react";
import Layout from "../../common/layouts/Layout";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import SearchActiveFilters from "modules/search/presentationals/SearchActiveFilters";
import RaisedButton from "material-ui/RaisedButton";
import SearchResults from "modules/search/presentationals/SearchResults";
import Sticky from "react-stickynode";
// import queryString from "qs";
import Modal from "react-awesome-modal";
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
        <Modal
          visible={this.state.showModal}
          width="300"
          height="200"
          effect="fadeInUp"
          onClickAway={() => this.setState({ showModal: false })}
        >
          <div className="has-text-centered section">
            Cette fonctionnalité sera bientôt disponible !
            <br />
            <br />
            <p>
              <a
                className="button is-primary"
                href="javascript:void(0);"
                onClick={() => this.setState({ showModal: false })}
              >
                OK
              </a>
            </p>
          </div>
        </Modal>
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
              <Sticky enabled={true} top={50}>
                <SearchFilters
                  defaultValues={this.props}
                  onFiltersChange={this.handlFiltersChange}
                />
              </Sticky>
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
