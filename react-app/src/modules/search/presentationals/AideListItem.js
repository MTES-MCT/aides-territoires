import React from "react";
import PropTypes from "prop-types";
import "./AideListItem.css";
import classNames from "classnames";
import AideListItemDetails from "./AideListItemDetails";
import { Motion, spring } from "react-motion";
import SlideDown from "modules/ui-kit/SlideDown";

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
        <p className="content">
          <em>{aide.description}</em>
        </p>
        <SlideDown maxHeight={400} show={this.state.showDetails}>
          <AideListItemDetails aide={aide} />
        </SlideDown>
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
