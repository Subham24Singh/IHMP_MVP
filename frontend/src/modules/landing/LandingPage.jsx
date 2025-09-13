// src/modules/landing/LandingPage.jsx
import React from "react";
// import Navbar from "./Navbar.jsx";
import Navbar from "./Navbar";
import HeroSection from "./HeroSection";
import StatsSection from "./StatsSection";
import FeaturesSection from "./FeaturesSection";
import BenefitsSection from "./BenefitsSection";
import CTASection from "./CTASection";
import Footer from "./Footer";

const LandingPage = () => {
  const handleGetStarted = (role) => {
    window.location.href = `/auth?role=${role}`;
  };

  return (
    <div>
      <Navbar onLogin={() => handleGetStarted("patient")} />
      <HeroSection onGetStarted={handleGetStarted} />
      <StatsSection />
      <FeaturesSection />
      <BenefitsSection />
      <CTASection onGetStarted={handleGetStarted} />
      <Footer />
    </div>
  );
};

export default LandingPage;