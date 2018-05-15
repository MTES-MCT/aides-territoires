import React from "react";
import Layout from "../../common/layouts/Layout";
import AideList from "modules/search/presentationals/AideList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import SearchActiveFilters from "modules/search/presentationals/SearchActiveFilters";
import AidesSearchQuery from "modules/search/decorators/AidesSearchQuery";
import RaisedButton from "material-ui/RaisedButton";
// import queryString from "qs";
import { connect } from "react-redux";
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
              <SearchFilters
                defaultValues={this.props}
                onFiltersChange={this.handlFiltersChange}
              />
            </div>
            <div className="column">
              {/*<SearchActiveFilters />*/}
              {this.props.perimetreApplicationType === "departement" && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"departement"}
                  perimetreApplicationCode={this.props.perimetreApplicationCode}
                  formeDeDiffusion={this.props.formeDeDiffusion}
                  etape={this.props.etape}
                  type={this.props.type}
                  thematiques={this.props.thematiques}
                  destination={this.props.destination}
                >
                  {({ aides }) => (
                    <div>
                      <AideList aides={aides} />
                    </div>
                  )}
                </AidesSearchQuery>
              )}
              {this.props.codeDepartement && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"departement"}
                  perimetreApplicationCode={this.props.codeDepartement}
                  formeDeDiffusion={this.props.formeDeDiffusion}
                  etape={this.props.etape}
                  type={this.props.type}
                  thematiques={this.props.thematiques}
                  destination={this.props.destination}
                >
                  {({ aides }) => (
                    <div>
                      <AideList aides={aides} />
                    </div>
                  )}
                </AidesSearchQuery>
              )}
              {this.props.codeRegion && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"region"}
                  perimetreApplicationCode={this.props.codeRegion}
                  formeDeDiffusion={this.props.formeDeDiffusion}
                  etape={this.props.etape}
                  type={this.props.type}
                  thematiques={this.props.thematiques}
                  destination={this.props.destination}
                >
                  {({ aides }) => (
                    <div>
                      <AideList aides={aides} />
                    </div>
                  )}
                </AidesSearchQuery>
              )}
              {this.props.perimetreApplicationType === "region" && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={this.props.perimetreApplicationType}
                  perimetreApplicationCode={this.props.perimetreApplicationCode}
                  formeDeDiffusion={this.props.formeDeDiffusion}
                  etape={this.props.etape}
                  type={this.props.type}
                  thematiques={this.props.thematiques}
                  destination={this.props.destination}
                >
                  {({ aides }) => (
                    <div>
                      <AideList aides={aides} />
                    </div>
                  )}
                </AidesSearchQuery>
              )}
              {(this.props.perimetreApplicationType === "commune" ||
                this.props.perimetreApplicationType === "departement") && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"departement"}
                  perimetreApplicationCode={""}
                  formeDeDiffusion={this.props.formeDeDiffusion}
                  etape={this.props.etape}
                  type={this.props.type}
                  thematiques={this.props.thematiques}
                  destination={this.props.destination}
                >
                  {({ aides }) => (
                    <div>
                      <AideList aides={aides} />
                    </div>
                  )}
                </AidesSearchQuery>
              )}
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"region"}
                perimetreApplicationCode={""}
                formeDeDiffusion={this.props.formeDeDiffusion}
                etape={this.props.etape}
                type={this.props.type}
                thematiques={this.props.thematiques}
                destination={this.props.destination}
              >
                {({ aides }) => (
                  <div>
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"outre_mer"}
                perimetreApplicationCode={""}
                formeDeDiffusion={this.props.formeDeDiffusion}
                etape={this.props.etape}
                type={this.props.type}
                thematiques={this.props.thematiques}
                destination={this.props.destination}
              >
                {({ aides }) => (
                  <div>
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"metropole"}
                perimetreApplicationCode={""}
                formeDeDiffusion={this.props.formeDeDiffusion}
                etape={this.props.etape}
                type={this.props.type}
                thematiques={this.props.thematiques}
                destination={this.props.destination}
              >
                {({ aides }) => (
                  <div>
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"france"}
                perimetreApplicationCode={""}
                formeDeDiffusion={this.props.formeDeDiffusion}
                etape={this.props.etape}
                type={this.props.type}
                thematiques={this.props.thematiques}
                destination={this.props.destination}
              >
                {({ aides }) => (
                  <div>
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
              <AidesSearchQuery
                statusPublication={["published"]}
                perimetreApplicationType={"europe"}
                perimetreApplicationCode={""}
                formeDeDiffusion={this.props.formeDeDiffusion}
                etape={this.props.etape}
                type={this.props.type}
                thematiques={this.props.thematiques}
                destination={this.props.destination}
              >
                {({ aides }) => (
                  <div>
                    <AideList aides={aides} />
                  </div>
                )}
              </AidesSearchQuery>
            </div>
          </div>
        </div>
      </Layout>
    );
  }
};

export default connect(state => {
  if (state.form.searchFilters && state.form.searchFilters.values) {
    return { ...state.form.searchFilters.values };
  }
  return {};
})(SearchAidePage);
