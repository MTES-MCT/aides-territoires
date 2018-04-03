import React from "react";
import DefaultLayout from "../../layouts/defaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import { List, ListItem, makeSelectable } from "material-ui/List";
import RaisedButton from "material-ui/RaisedButton";
import PropTypes from "prop-types";

const style = {
  margin: 12
};

let SelectableList = makeSelectable(List);

function wrapState(ComposedComponent) {
  return class SelectableList extends React.Component {
    static propTypes = {
      children: PropTypes.node.isRequired,
      defaultValue: PropTypes.number.isRequired
    };

    componentWillMount() {
      this.setState({
        selectedIndex: this.props.defaultValue
      });
    }

    handleRequestChange = (event, index) => {
      this.setState({
        selectedIndex: index
      });
    };

    render() {
      return (
        <ComposedComponent
          value={this.state.selectedIndex}
          onChange={this.handleRequestChange}
        >
          {this.props.children}
        </ComposedComponent>
      );
    }
  };
}

SelectableList = wrapState(SelectableList);

class ParcoursPhase extends React.Component {
  onSearchSubmit = () => {
    alert("ok");
  };
  render() {
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section">
            <div className="has-text-centered">
              <SelectableList defaultValue={3}>
                <ListItem
                  value={1}
                  primaryText="Avant projet"
                  secondaryText="description de la phase"
                />
                <ListItem
                  value={2}
                  primaryText="programmation, conception et réalisation"
                  secondaryText="description de la phase"
                />
                <ListItem
                  value={3}
                  primaryText="fonctionnement"
                  secondaryText="description de la phase"
                />
              </SelectableList>
              <Link to="/">
                <RaisedButton
                  style={style}
                  label="Précédent"
                  secondary={true}
                />
              </Link>
              <Link to="/">
                <RaisedButton style={style} label="Suivant" primary={true} />
              </Link>
            </div>
          </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursPhase;
