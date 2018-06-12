import Document, { meta } from "../content/index.md";
import DocumentContact from "../content/contactez-nous.md";
import Header from "../components/ui/Header";
import ButtonLink from "../components/ui/ButtonLink";
import Section from "../components/ui/Section";
import backgroundImageUrl from "../static/images/header.png";
import Layout from "../components/ui/Layout";
import Container from "../components/ui/Container";
import Steps from "../components/ui/Steps";
import uiConfig from "../ui.config";
import injectSheet from "react-jss";
import SendInBlueInscrivezVous from "../components/ui/SendInBlueInscrivezVous";

const Index = ({ classes }) => {
  return (
    <Layout>
      <Header
        backgroundImageUrl={backgroundImageUrl}
        title={meta.header.title}
        subtitle={meta.header.subtitle}
        callToActionText={meta.header.callToAction.text}
        callToActionLink={meta.header.callToAction.link}
      />
      <Section>
        <Container>
          <h3
            style={{
              textAlign: "center",
              color: uiConfig.colors.primary,
              paddingBottom: "2rem"
            }}
          >
            {meta.sectionCommentCaMarche.title}
          </h3>
          <Steps steps={meta.sectionCommentCaMarche.steps} />
        </Container>
      </Section>
      <Section backgroundColor="primary">
        <Container>
          <p style={{ fontSize: "25px", fontWeight: "500" }}>
            {meta.sectionPainPoint.title}
          </p>
          <p style={{ fontSize: "25px", color: "white", fontWeight: "500" }}>
            {meta.sectionPainPoint.question}
          </p>
        </Container>
      </Section>
      <Section>
        <Container>
          <div style={{ fontSize: "25px" }}>{meta.sectionBenefices.title}</div>
          <ul style={{ fontSize: "25px" }}>
            {meta.sectionBenefices.points.map((point, index) => {
              return <li key={index}>{point}</li>;
            })}
          </ul>
        </Container>
      </Section>
      <div
        style={{
          background: "linear-gradient(#3585A7, #021D58)",
          paddingTop: "2rem"
        }}
      >
        <p
          style={{
            fontSize: "20px",
            fontWeight: "800",
            color: uiConfig.colors.light,
            textAlign: "center"
          }}
        >
          {meta.sendInBlueForm.description}
        </p>
        <SendInBlueInscrivezVous />
      </div>
      <Section>
        <Container>
          <div id="contact">
            <div
              style={{
                color: uiConfig.colors.dark,
                textAlign: "center"
              }}
            >
              <DocumentContact />
            </div>
          </div>
        </Container>
      </Section>
    </Layout>
  );
};

export default Index;
