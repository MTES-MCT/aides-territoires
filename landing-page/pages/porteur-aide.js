import React from "react";
import DefaultLayout from "../components/DefaultLayout";
import HeaderPorteurAide from "../components/HeaderPorteurAide";
import SectionCommentCaMarche from "../components/SectionCommentCaMarche";
import SectionChronophage from "../components/SectionChronophage";
import SectionBenefices from "../components/SectionBenefices";
import SectionTypeAides from "../components/SectionTypesAides";
import SectionPorteurAideDescription from "../components/SectionPorteurAideDescription";
import SendInBlueInscrivezVous from "../components/SendInBlueInscrivezVous";
import SendInBlueContactForm from "../components/SendInBlueContactForm";

class porteurAidePage extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <HeaderPorteurAide />
        <SectionPorteurAideDescription />
      </DefaultLayout>
    );
  }
}

export default porteurAidePage;
