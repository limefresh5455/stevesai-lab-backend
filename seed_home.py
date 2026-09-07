import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Create an engine to the specific db
engine = create_engine("postgresql://stevesai:password123@localhost:5433/stevesai_cms")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from app.models.content import Page
from app.models.admin import Admin
from app.database import Base

Base.metadata.create_all(bind=engine)

existing = db.query(Page).filter(Page.slug == "home").first()

DEFAULT_JSON = {
  "hero": {
    "titlePrefix": "Engineering the Future with a Custom",
    "titleHighlight": "Software Development Company",
    "description": "As a leading custom software development company, we develop AI solutions by combining foundational models, data-driven insights, and up-to-date architecture so that they can grow with your business.",
    "bgImage": "/images/hero-bg.png",
    "upworkScore": "100%",
    "upworkText": "Success score",
    "clutchScore": "4.9/5",
    "clutchText": "Achieved"
  },
  "trustBenefits": [
    {
      "title": "Transparent AI Lifecycles",
      "description": "No black box. Slack channels, weekly model training updates and 100% transparent deployment timelines, directly.",
      "image": "/images/Transparent.png"
    },
    {
      "title": "6 Months Free Maintenance",
      "description": "With every custom AI deployment, you get 6 months of free monitoring, bug fixes and post-launch support.",
      "image": "/images/Maintenance.png"
    },
    {
      "title": "Bespoke Neural Models",
      "description": "Zero generic wrappers. From base LLMs to complex applications, everything is built for your enterprise.",
      "image": "/images/Bespoke.png"
    },
    {
      "title": "20 Hours Free QA Testing",
      "description": "Start with confidence. We offer 20 hours of AI testing, QA and cloud managed services for a secure launch.",
      "image": "/images/Free-QA.png"
    },
    {
      "title": "Enterprise-Grade Security",
      "description": "Your proprietary data stays yours. We implement strict encryption and private cloud protocols.",
      "image": "/images/Enterprise.png"
    },
    {
      "title": "Dedicated AI Strategist",
      "description": "Your architecture is guided from initial data discovery to flawless final execution by an experienced project lead.",
      "image": "/images/Strategist.png"
    },
    {
      "title": "Future-Proof Scalability",
      "description": "Modern infrastructures ensure that your AI can handle increasing users and data volumes.",
      "image": "/images/Future-Proof.png"
    }
  ],
  "processSection": {
    "titlePrefix": "How We Build Trust & Deliver",
    "titleHighlight": "Enterprise AI Excellence",
    "description": "Enterprise AI Solutions. Transform complex data into scalable, high-performance intelligent systems with a transparent, end-to-end engineering lifecycle.",
    "steps": [
      {
        "num": "01",
        "title": "Discovery & Strategic Analysis",
        "desc": "We dive deep into your business objectives to define the AI strategy and roadmap."
      },
      {
        "num": "02",
        "title": "Data Architecture & Processing",
        "desc": "Structuring and refining your data to ensure high-quality model training and inference."
      },
      {
        "num": "03",
        "title": "Model Engineering & Training",
        "desc": "Building, fine-tuning, and optimizing neural networks and LLMs for your specific use cases."
      },
      {
        "num": "04",
        "title": "Stress Testing & Deployment",
        "desc": "Rigorous QA testing for security, scalability, and performance before going live."
      },
      {
        "num": "05",
        "title": "Integration & Interface Design",
        "desc": "Seamlessly connecting AI capabilities with modern, intuitive user interfaces."
      }
    ]
  },
  "industriesSection": {
    "title": "Industries",
    "industries": [
      "Cypress",
      "UCLA",
      "Infotech",
      "Capmark",
      "Visualsoft",
      "Cadence"
    ],
    "testimonials": [
      {
        "text": "The custom ML architecture they built for us was incredible. Their lightning-fast execution allowed us to rapidly optimize our proprietary algorithms and deploy to production months ahead of schedule.",
        "name": "David T.",
        "role": "Technical Lead, Cypress"
      },
      {
        "text": "Handling our massive datasets required highly tailored AI infrastructure. Steves AI Lab delivered with unparalleled professionalism, engineering custom solutions perfectly suited to our complex research needs.",
        "name": "Michael C.",
        "role": "Data Science Director, UCLA"
      },
      {
        "text": "A true game-changer. They seamlessly transitioned our complex machine learning concepts into a flawless, production-ready AI product.",
        "name": "Rebecca L.",
        "role": "VP of Engineering, Infotech"
      },
      {
        "text": "Their deep understanding of AI is matched only by their UI/UX expertise. They successfully translated our complex algorithmic vision into a cutting-edge web application.",
        "name": "Sarah J.",
        "role": "Product Manager, Capmark"
      },
      {
        "text": "Their team of AI engineers and UI designers are true innovators. They pushed the boundaries of what's technologically possible and delivered a highly scalable solution.",
        "name": "Emily R.",
        "role": "Director of Product, Visualsoft"
      },
      {
        "text": "Their custom generative models completely transformed our data pipelines, automating hundreds of hours of manual processing with flawless precision.",
        "name": "Marcus V.",
        "role": "Chief Technology Officer, Cadence"
      }
    ]
  },
  "metricsSection": [
    { "value": 150, "suffix": "+", "label": "Projects Delivered" },
    { "value": 10, "suffix": "+", "label": "Years of Experience" },
    { "value": 45, "suffix": "+", "label": "AI Experts" },
    { "value": 99, "suffix": "%", "label": "Client Satisfaction" }
  ],
  "capabilitiesSection": [
    { "slug": "ai-machine-learning", "title": "AI & Machine Learning", "desc": "Custom predictive models and advanced data analytics systems.", "icon": "Brain" },
    { "slug": "llm-services", "title": "LLM Services", "desc": "Fine-tuned language models and robust RAG architectures.", "icon": "Sparkles" },
    { "slug": "generative-ai", "title": "Generative AI", "desc": "Automated content creation and specialized diffusion models.", "icon": "Layers" },
    { "slug": "foundation-models", "title": "Foundation Models", "desc": "Pretrained systems customized for enterprise use cases.", "icon": "Cpu" },
    { "slug": "application-development", "title": "Application Development", "desc": "High-performance web and mobile software engineering.", "icon": "Code" },
    { "slug": "cloud-services", "title": "Cloud Services", "desc": "Scalable infrastructure and secure MLOps deployment.", "icon": "Cloud" }
  ],
  "faqSection": [
    {
      "q": "What is Steve's AI Lab?",
      "a": "We are a specialized engineering firm focused on custom software development, artificial intelligence, and enterprise cloud solutions."
    },
    {
      "q": "Custom systems vs templates?",
      "a": "We build tailored architectures from the ground up to ensure they scale exactly to your unique business logic, rather than forcing you into rigid templates."
    },
    {
      "q": "What is your development process?",
      "a": "We follow a 5-step process: Discovery, Data Architecture, Model Engineering, Stress Testing, and Integration."
    },
    {
      "q": "Do you offer post-launch support?",
      "a": "Yes, we include 6 months of free maintenance and comprehensive support SLAs to ensure your systems run flawlessly."
    },
    {
      "q": "How do you handle data security?",
      "a": "We implement enterprise-grade security protocols, end-to-end encryption, and rigorous compliance checks throughout the data lifecycle."
    }
  ]
}

if not existing:
    new_page = Page(
        title="Home",
        slug="home",
        content=DEFAULT_JSON,
        status="published"
    )
    db.add(new_page)
    db.commit()
    print("Successfully seeded home page!")
else:
    existing.content = DEFAULT_JSON
    db.commit()
    print("Successfully updated home page!")

db.close()
