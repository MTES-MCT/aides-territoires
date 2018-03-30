import React from "react";
import DefaultLayout from "../components/common/DefaultLayout";
import Header from "../components/index/Header";
import CommentCaMarche from "../components/index/CommentCaMarche";
import Chronophage from "../components/index/Chronophage";
import Benefices from "../components/index/Benefices";
import TypeAides from "../components/index/TypesAides";
import FormPorteurProjetQuartierDurable from "../components/index/FormPorteurProjetQuartierDurable";
import ContactForm from "../components/common/ContactForm";
import graphcms from "../services/graphcms";

class HomePage extends React.Component {
  static async getInitialProps({ req }) {
    const query = `{
      Pagedaccueil(id:"cjfdxk4tpcy3v016424h68se6") {
        commentcamarchetitre
        commentcamarchebloc1
        commentcamarchebloc2
        commentcamarchebloc3
        commentcamarchebloc1titre
        commentcamarchebloc2titre
        commentcamarchebloc3titre
        header
        headercalltoaction
        headertitre
        probleme
        benefices
        texteduformulaireaideecoquartiers
        texteduformulairedecontact
      }
    }
    `;
    return graphcms.request(query);
  }
  render() {
    return (
      <DefaultLayout>
        <Header data={this.props.Pagedaccueil} />
        <CommentCaMarche data={this.props.Pagedaccueil} />
        <Chronophage data={this.props.Pagedaccueil} />
        <Benefices data={this.props.Pagedaccueil} />
        {/* <TypeAides /> */}
        <FormPorteurProjetQuartierDurable data={this.props.Pagedaccueil} />
        <ContactForm data={this.props.Pagedaccueil} />
      </DefaultLayout>
    );
  }
}

export default HomePage;
