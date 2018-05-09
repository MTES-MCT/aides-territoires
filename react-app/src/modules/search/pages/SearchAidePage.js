import React from "react";
import Layout from "../../common/layouts/Layout";
import AideList from "modules/search/presentationals/AideList";
import SearchFilters from "modules/search/presentationals/SearchFilters";
import AidesSearchQuery from "modules/search/decorators/AidesSearchQuery";
import RaisedButton from "material-ui/RaisedButton";
import queryString from "qs";
import "./SearchAidePage.css";

const SearchAidePage = class extends React.Component {
  state = {
    type: [],
    etape: [],
    perimetreApplicationType: [],
    formeDeDiffusion: "",
    // texte du moteur de recherche
    searchedText: ""
  };
  constructor(props) {
    super(props);
    const urlParams = queryString.parse(props.location.search);
    this.state = {
      ...urlParams
    };
  }
  handlFiltersChange = newValues => {
    this.setState({
      ...newValues.values
    });
  };
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
                defaultValues={this.state}
                onFiltersChange={this.handlFiltersChange}
              />
            </div>
            <div className="column">
              {this.state.perimetreApplicationType === "departement" && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"departement"}
                  perimetreApplicationCode={this.state.perimetreApplicationCode}
                  formeDeDiffusion={this.state.formeDeDiffusion}
                  etape={this.state.etape}
                  type={this.state.type}
                  thematiques={this.state.thematiques}
                  destination={this.state.destination}
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
              {this.state.codeDepartement && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"departement"}
                  perimetreApplicationCode={this.state.codeDepartement}
                  formeDeDiffusion={this.state.formeDeDiffusion}
                  etape={this.state.etape}
                  type={this.state.type}
                  thematiques={this.state.thematiques}
                  destination={this.state.destination}
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
              {this.state.codeRegion && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"region"}
                  perimetreApplicationCode={this.state.codeRegion}
                  formeDeDiffusion={this.state.formeDeDiffusion}
                  etape={this.state.etape}
                  type={this.state.type}
                  thematiques={this.state.thematiques}
                  destination={this.state.destination}
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
              {this.state.perimetreApplicationType === "region" && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={this.state.perimetreApplicationType}
                  perimetreApplicationCode={this.state.perimetreApplicationCode}
                  formeDeDiffusion={this.state.formeDeDiffusion}
                  etape={this.state.etape}
                  type={this.state.type}
                  thematiques={this.state.thematiques}
                  destination={this.state.destination}
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
              {(this.state.perimetreApplicationType === "commune" ||
                this.state.perimetreApplicationType === "departement") && (
                <AidesSearchQuery
                  statusPublication={["published"]}
                  perimetreApplicationType={"departement"}
                  perimetreApplicationCode={""}
                  formeDeDiffusion={this.state.formeDeDiffusion}
                  etape={this.state.etape}
                  type={this.state.type}
                  thematiques={this.state.thematiques}
                  destination={this.state.destination}
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
                formeDeDiffusion={this.state.formeDeDiffusion}
                etape={this.state.etape}
                type={this.state.type}
                thematiques={this.state.thematiques}
                destination={this.state.destination}
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
                formeDeDiffusion={this.state.formeDeDiffusion}
                etape={this.state.etape}
                type={this.state.type}
                thematiques={this.state.thematiques}
                destination={this.state.destination}
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
                formeDeDiffusion={this.state.formeDeDiffusion}
                etape={this.state.etape}
                type={this.state.type}
                thematiques={this.state.thematiques}
                destination={this.state.destination}
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
                formeDeDiffusion={this.state.formeDeDiffusion}
                etape={this.state.etape}
                type={this.state.type}
                thematiques={this.state.thematiques}
                destination={this.state.destination}
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
                formeDeDiffusion={this.state.formeDeDiffusion}
                etape={this.state.etape}
                type={this.state.type}
                thematiques={this.state.thematiques}
                destination={this.state.destination}
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

export default SearchAidePage;
