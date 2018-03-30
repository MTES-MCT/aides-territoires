import React from "react";
import DefaultLayout from "../components/common/DefaultLayout";
import Header from "../components/a-propos/Header";
import Content from "../components/a-propos/Content";
import Equipe from "../components/a-propos/Equipe";
import graphcms from "../services/graphcms";

class aProposPage extends React.Component {
  static async getInitialProps({ req }) {
    const query = `{
      Apropos(id: "cjfe3t8sd93c40163rxtde3go") {
        contenu
        lesprochainesetapes
        presentationElise
        presentationRoxane
        presentationYann
        textedublocequipe
        texteduheader
        titredansleheader
        titredublocequipe
      }
    }    
    `;
    return graphcms.request(query);
  }
  render() {
    return (
      <DefaultLayout>
        <Header data={this.props.Apropos} />
        <Content data={this.props.Apropos} />
        <Equipe data={this.props.Apropos} />
      </DefaultLayout>
    );
  }
}

export default aProposPage;
