import React from "react";
import DefaultLayout from "../../../../app/components/layouts/defaultLayout/DefaultLayout";
import SearchFormContainer from "../../../../search/components/containers/searchFormContainer/SearchFormContainer";
import { Link } from "react-router-dom";

const STEP_LOCALISATION = "localisation";
const STEP_PHASE = "phase";
const STEP_AIDES = "aides";

class ParcoursPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentStep: STEP_LOCALISATION
    };
  }
  onSearchSubmit = () => {
    alert("ok");
  };
  render() {
    const step = this.props.match.params.step || STEP_LOCALISATION;
    return (
      <DefaultLayout>
        <section className="section container">
          <ParcoursSteps />
        </section>
        <div className="container">
          {step === STEP_LOCALISATION && (
            <section className="section has-text-centered">
              <h2 className="title is-2">Votre localisation</h2>
              <h2 className="subtitle is-2">
                Commune, département, région ...
              </h2>
              <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
            </section>
          )}
          {step === STEP_PHASE && (
            <section className="section">
              <h2 className="title has-text-centered is-2">
                Où en est votre projet ?
              </h2>
              <div className="media">
                <div className="media-left">
                  <img width="200px" src="/step-phase-1.jpg" />
                </div>
                <div className="media-content">
                  Baruch/Bento/Benedictus Spinoza/de Spinoza/de
                  Espinosa/d'Espinozaa, né le 24 novembre 1632 à Amsterdam et
                  mort le 21 février 1677 à La Haye, est un philosophe
                  néerlandais d'origine portugaise dont la pensée eut une
                  influence considérable sur ses contemporains et nombre de
                  penseurs postérieurs.
                </div>
              </div>
              <div className="media">
                <div className="media-left">
                  <img width="200px" src="/step-phase-1.jpg" />
                </div>
                <div className="media-content">
                  Baruch/Bento/Benedictus Spinoza/de Spinoza/de
                  Espinosa/d'Espinozaa, né le 24 novembre 1632 à Amsterdam et
                  mort le 21 février 1677 à La Haye, est un philosophe
                  néerlandais d'origine portugaise dont la pensée eut une
                  influence considérable sur ses contemporains et nombre de
                  penseurs postérieurs.
                </div>
              </div>
              <div className="media">
                <div className="media-left">
                  <img width="200px" src="/step-phase-1.jpg" />
                </div>
                <div className="media-content">
                  Baruch/Bento/Benedictus Spinoza/de Spinoza/de
                  Espinosa/d'Espinozaa, né le 24 novembre 1632 à Amsterdam et
                  mort le 21 février 1677 à La Haye, est un philosophe
                  néerlandais d'origine portugaise dont la pensée eut une
                  influence considérable sur ses contemporains et nombre de
                  penseurs postérieurs.
                </div>
              </div>
            </section>
          )}
          {step === STEP_AIDES && (
            <section className="section">
              <h2 className="title has-text-centered is-2">
                Les aides que vous pouvez mobiliser
              </h2>
            </section>
          )}
        </div>
      </DefaultLayout>
    );
  }
}

class ParcoursSteps extends React.Component {
  render() {
    return (
      <div>
        <progress class="progress is-success" value="90" max="100">
          90%
        </progress>
        <nav className="level is-primary">
          <div className="level-item has-text-centered">
            <div>
              <Link to="/parcours/localisation" className="link is-info">
                Localisation
              </Link>
            </div>
          </div>
          <div className="level-item has-text-centered">
            <div>
              <Link to="/parcours/phase" className="link is-info">
                Phase
              </Link>
            </div>
          </div>
          <div className="level-item has-text-centered">
            <div>
              <Link to="/parcours/aides" className="link is-info">
                Vos aides
              </Link>
            </div>
          </div>
        </nav>
      </div>
    );
  }
}

export default ParcoursPage;
