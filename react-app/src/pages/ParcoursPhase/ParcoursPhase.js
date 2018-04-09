import React from "react";
import DefaultLayout from "../../layouts/DefaultLayout/DefaultLayout";
import { Link } from "react-router-dom";
import { List, ListItem, makeSelectable } from "material-ui/List";
import RaisedButton from "material-ui/RaisedButton";

const style = {
  margin: 12
};

let SelectableList = makeSelectable(List);

class ParcoursPhase extends React.Component {
  componentWillMount() {
    this.setState({
      selectedIndex: null,
      LinkTo: ""
    });
  }
  getLinkToFromIndex(index) {
    const map = {
      1: "/parcours/phase/avant-projet",
      2: "/parcours/phase/xxx",
      3: "/parcours/phase/xyz"
    };
    return map[index];
  }

  handleRequestChange = (event, index) => {
    this.setState({
      selectedIndex: index,
      LinkTo: this.getLinkToFromIndex(index)
    });
  };
  render() {
    const RaisedButtonProps = {};
    if (this.state.LinkTo === "") {
      RaisedButtonProps.disabled = true;
    }
    return (
      <DefaultLayout>
        <div className="container">
          <section className="section">
            <div className="has-text-centered">
              <SelectableList
                onChange={this.handleRequestChange}
                value={this.state.selectedIndex}
              >
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
              <Link to={this.state.LinkTo}>
                <RaisedButton
                  {...RaisedButtonProps}
                  style={style}
                  label="Suivant"
                  primary={true}
                />
              </Link>
            </div>
          </section>
        </div>
      </DefaultLayout>
    );
  }
}

export default ParcoursPhase;
