import React from "react";
import Layout from "../../common/layouts/Layout";
import AideList from "modules/search/presentationals/AideList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import ActiveFilters from "modules/search/presentationals/ActiveFilters";
import AidesSearchQuery from "modules/search/decorators/AidesSearchQuery";
import RaisedButton from "material-ui/RaisedButton";
import queryString from "qs";
import { connect } from "react-redux";
import "./SearchAidePage.css";

const SearchAidePage = class extends React.Component {
  /*
  constructor(props) {
    super(props);
    const urlParams = queryString.parse(props.location.search);
    this.props = {
      ...urlParams
    };
  }
  */
  render() {
    return (
      <Layout>
        <div style={{ textAlign: "right", marginTop: "2rem" }}>
          <RaisedButton
            style={{ marginRight: "20px" }}
            primary={true}
            label="Imprimer mes résultats"
          />
          <RaisedButton
            style={{ marginRight: "20px" }}
            secondary={true}
            label="Partager mes résultats"
          />
          <RaisedButton
            style={{ marginRight: "20px" }}
            label="Etre alerté de nouvelles aides"
          />
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
              <ActiveFilters />
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
                      {aides.length > 0 && (
                        <h2 className="title is-2">
                          A destination de votre département
                        </h2>
                      )}
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
                      {aides.length > 0 && (
                        <h2 className="title is-2">
                          A destination de votre département
                        </h2>
                      )}
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
                      {aides.length > 0 && (
                        <h2 className="title is-2">
                          A destination de votre région
                        </h2>
                      )}
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
                      {aides.length > 0 && (
                        <h2 className="title is-2">
                          A destination de votre région
                        </h2>
                      )}
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
                      {aides.length > 0 && (
                        <h2 className="title is-2">
                          Toutes les aides départementales
                        </h2>
                      )}
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
                    {aides.length > 0 && (
                      <h2 className="title is-2">
                        Toutes les aides régionales
                      </h2>
                    )}
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
                    {aides.length > 0 && (
                      <h2 className="title is-2">Outre mer</h2>
                    )}
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
                    {aides.length > 0 && (
                      <h2 className="title is-2">Métropole</h2>
                    )}
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
                    {aides.length > 0 && (
                      <h2 className="title is-2">
                        Toutes les aides nationales
                      </h2>
                    )}
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
                    {aides.length > 0 && (
                      <h2 className="title is-2">
                        Toutes les aides européennes
                      </h2>
                    )}
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
