import React from "react";
import Layout from "../layouts/Layout";
import Header from "../ui/Header";
import Benefices from "./HomepageBenefices";
import CommentCaMarche from "./HomepageCommentCaMarche";
import Chronophage from "./HomepageChronophage";
import graphcms from "../../lib/graphcms";

class HomePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      Pagedaccueil: {}
    };
  }
  componentWillMount() {
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
    graphcms.request(query).then(Pagedaccueil => {
      this.setState(Pagedaccueil);
    });
  }
  render() {
    const Pagedaccueil = this.state.Pagedaccueil;
    return (
      <Layout>
        <Header data={Pagedaccueil} />
        <CommentCaMarche data={Pagedaccueil} />
        <Chronophage data={Pagedaccueil} />
        <Benefices data={Pagedaccueil} />
      </Layout>
    );
  }
}

export default HomePage;
