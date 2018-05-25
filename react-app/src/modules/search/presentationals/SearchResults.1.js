import React from "react";
import AidesSearchQuery from "modules/search/decorators/AidesSearchQuery";
import AideList from "modules/search/presentationals/AideList";
import { connect } from "react-redux";

const SearchResults = props => {
  return (
    <div>
      <div className="notification">
        Par défaut, le moteur de recherche présente toutes les aides disponibles
        sur votre territoire.Vous pouvez utiliser les filtres ci-contre pour
        préciser votre recherche et sélectionner vos critères
      </div>
      {props.perimetreApplicationType === "departement" && (
        <AidesSearchQuery
          statusPublication={["published"]}
          perimetreApplicationType={"departement"}
          perimetreApplicationCode={props.perimetreApplicationCode}
          formeDeDiffusion={props.formeDeDiffusion}
          etape={props.etape}
          type={props.type}
          thematiques={props.thematiques}
          destination={props.destination}
        >
          {({ aides }) => (
            <div>
              <AideList aides={aides} />
            </div>
          )}
        </AidesSearchQuery>
      )}
      {props.codeDepartement && (
        <AidesSearchQuery
          statusPublication={["published"]}
          perimetreApplicationType={"departement"}
          perimetreApplicationCode={props.codeDepartement}
          formeDeDiffusion={props.formeDeDiffusion}
          etape={props.etape}
          type={props.type}
          thematiques={props.thematiques}
          destination={props.destination}
        >
          {({ aides }) => (
            <div>
              <AideList aides={aides} />
            </div>
          )}
        </AidesSearchQuery>
      )}
      {props.codeRegion && (
        <AidesSearchQuery
          statusPublication={["published"]}
          perimetreApplicationType={"region"}
          perimetreApplicationCode={props.codeRegion}
          formeDeDiffusion={props.formeDeDiffusion}
          etape={props.etape}
          type={props.type}
          thematiques={props.thematiques}
          destination={props.destination}
        >
          {({ aides }) => (
            <div>
              <AideList aides={aides} />
            </div>
          )}
        </AidesSearchQuery>
      )}
      {props.perimetreApplicationType === "region" && (
        <AidesSearchQuery
          statusPublication={["published"]}
          perimetreApplicationType={props.perimetreApplicationType}
          perimetreApplicationCode={props.perimetreApplicationCode}
          formeDeDiffusion={props.formeDeDiffusion}
          etape={props.etape}
          type={props.type}
          thematiques={props.thematiques}
          destination={props.destination}
        >
          {({ aides }) => (
            <div>
              <AideList aides={aides} />
            </div>
          )}
        </AidesSearchQuery>
      )}
      {(props.perimetreApplicationType === "commune" ||
        props.perimetreApplicationType === "departement") && (
        <AidesSearchQuery
          statusPublication={["published"]}
          perimetreApplicationType={"departement"}
          perimetreApplicationCode={""}
          formeDeDiffusion={props.formeDeDiffusion}
          etape={props.etape}
          type={props.type}
          thematiques={props.thematiques}
          destination={props.destination}
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
        formeDeDiffusion={props.formeDeDiffusion}
        etape={props.etape}
        type={props.type}
        thematiques={props.thematiques}
        destination={props.destination}
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
        formeDeDiffusion={props.formeDeDiffusion}
        etape={props.etape}
        type={props.type}
        thematiques={props.thematiques}
        destination={props.destination}
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
        formeDeDiffusion={props.formeDeDiffusion}
        etape={props.etape}
        type={props.type}
        thematiques={props.thematiques}
        destination={props.destination}
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
        formeDeDiffusion={props.formeDeDiffusion}
        etape={props.etape}
        type={props.type}
        thematiques={props.thematiques}
        destination={props.destination}
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
        formeDeDiffusion={props.formeDeDiffusion}
        etape={props.etape}
        type={props.type}
        thematiques={props.thematiques}
        destination={props.destination}
      >
        {({ aides }) => (
          <div>
            <AideList aides={aides} />
          </div>
        )}
      </AidesSearchQuery>
    </div>
  );
};

export default connect(state => {
  if (state.form.searchFilters && state.form.searchFilters.values) {
    return { ...state.form.searchFilters.values };
  }
  return {};
})(SearchResults);
