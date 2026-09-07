import re
with open('src/components/sections/IndustriesSection.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'export default function IndustriesSection({ data }: { data?: any }) {',
    '''export default function IndustriesSection({ data }: { data?: any }) {
  const activeIndustries = data?.industries?.length > 0 ? data.industries : industries;
  const activeTestimonials = data?.testimonials?.length > 0 ? data.testimonials : testimonials;
  const titlePrefix = data?.titlePrefix || "Proven Across";
  const titleHighlight = data?.titleHighlight || "Complex Industries";
  const desc = data?.description || "We construct intelligent digital infrastructure for global technology companies and leading research institutions which is capable of meeting strict demands and promotes exponential growth.";'''
)

content = content.replace('industries.map', 'activeIndustries.map')
content = content.replace('testimonials.map', 'activeTestimonials.map')
content = content.replace('testimonials.length', 'activeTestimonials.length')
content = content.replace('Proven Across', '{titlePrefix}')
content = content.replace('Complex Industries', '{titleHighlight}')
content = content.replace('We construct intelligent digital infrastructure for global\n              technology companies and leading research institutions which is\n              capable of meeting strict demands and promotes exponential growth.', '{desc}')

with open('src/components/sections/IndustriesSection.tsx', 'w') as f:
    f.write(content)
