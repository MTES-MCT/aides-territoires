import React from "react";
import { List, ListItem } from "material-ui/List";
import Subheader from "material-ui/Subheader";
import Divider from "material-ui/Divider";
import Checkbox from "material-ui/Checkbox";
import Toggle from "material-ui/Toggle";

const styles = {
  root: {
    background: `rgb(250, 250, 250)`,
    display: "flex",
    flexWrap: "wrap"
  },
  subHeader: {
    fontSize: "20px",
    color: "black"
  }
};

const SearchFilters = () => (
  <div style={styles.root}>
    <div>
      <List>
        <Subheader style={{ fontSize: "25px", color: "black" }}>
          Filtres
        </Subheader>
      </List>
      <Divider />
      <List>
        <Subheader style={styles.subHeader}>Type d'aide</Subheader>
        <ListItem leftCheckbox={<Checkbox />} primaryText="financement" />
        <ListItem leftCheckbox={<Checkbox />} primaryText="ingénierie" />
        <ListItem leftCheckbox={<Checkbox />} primaryText="autre" />
      </List>
      <Divider />
      <List>
        <Subheader style={styles.subHeader}>
          Étape à laquelle mobiliser l'aide
        </Subheader>
        <ListItem primaryText="pré-opérationnel" leftCheckbox={<Checkbox />} />
        <ListItem primaryText="opérationnel" leftCheckbox={<Checkbox />} />
        <ListItem
          primaryText="Phase de vie / fonctionnement"
          leftCheckbox={<Checkbox />}
        />
      </List>
      <Divider />
      <List>
        <Subheader style={styles.subHeader}>Destination de l'aide</Subheader>
        <ListItem primaryText="études" leftCheckbox={<Checkbox />} />
        <ListItem primaryText="investissement" leftCheckbox={<Checkbox />} />
        <ListItem primaryText="travaux" leftCheckbox={<Checkbox />} />
      </List>
      <List>
        <Subheader style={styles.subHeader}>
          Forme de diffusion de l'aide
        </Subheader>
        <ListItem primaryText="subvention" leftCheckbox={<Checkbox />} />
        <ListItem primaryText="ingénierie" leftCheckbox={<Checkbox />} />
        <ListItem primaryText="valorisaion" leftCheckbox={<Checkbox />} />
      </List>
      <Divider />
      <List>
        <Subheader style={styles.subHeader}>
          Périmètre de diffusion de l'aide
        </Subheader>
      </List>
      <Divider />
      <List>
        <Subheader style={styles.subHeader}>Structure porteuse</Subheader>
      </List>
    </div>
  </div>
);

export default SearchFilters;
