import React from "react";
import PropTypes from "prop-types";
import AideListItemDetails from "./AideListItemDetails";
import SlideDown from "modules/ui-kit/reactMotion/SlideDown";
import Fade from "modules/ui-kit/reactMotion/Fade";
import { Spring, Transition } from "react-spring";
import "./AideListItem.css";

const DESCRIPTION_CHARS_LIMIT = 300;

class AideListItem extends React.Component {
  state = {
    showDetails: false
  };
  static propTypes = {
    aide: PropTypes.object.isRequired
  };
  handleMoreButtonClick = () => {
    this.setState(prevState => ({
      showDetails: !prevState.showDetails
    }));
  };
  render() {
    const { aide } = this.props;
    return (
      <div className="AideListItem search-result-list-item box">
        <h2 className="title is-4">{aide.nom}</h2>
        <p className="description">
          {aide.description.substring(0, DESCRIPTION_CHARS_LIMIT)}
          {!this.state.showDetails &&
            aide.description.length > DESCRIPTION_CHARS_LIMIT &&
            "..."}
          <Fade show={this.state.showDetails}>
            {aide.description.substring(DESCRIPTION_CHARS_LIMIT)}
          </Fade>
        </p>
        <Spring
          from={{ maxHeight: 0, overflow: "hidden" }}
          to={{
            maxHeight: this.state.showDetails ? 500 : 0
          }}
        >
          {styles => (
            <div style={styles}>
              <AideListItemDetails aide={aide} />
            </div>
          )}
        </Spring>
        <div className="show-more">
          <button onClick={this.handleMoreButtonClick} className="button">
            {!this.state.showDetails ? "Voir plus" : "cacher les détails"}
          </button>
        </div>
      </div>
    );
  }
}

export default AideListItem;
